from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from backend.app.schemas.query import QueryRequest, QueryResponse
from backend.app.core.graph import app as graph_app
from backend.app.api.v1.deps import get_current_user
from backend.app.core.database import get_supabase_client
from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import json
import re
from backend.services.logger import get_logger
from backend.services.chat_history import ChatHistoryService

logger = get_logger(__name__)
history_service = ChatHistoryService()
router = APIRouter()

# Schema for Stream (similar to main.py ChatRequest)
class StreamRequest(BaseModel):
    message: str
    history: Optional[list] = []
    session_id: Optional[str] = None
    user_id: Optional[str] = None

@router.post("/", response_model=QueryResponse)
async def create_query(
    request: QueryRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    supabase = get_supabase_client()
    query_id = None
    
    try:
        # 1. Create Initial Query Record (Pending)
        query_data = {
            "user_id": current_user["id"],
            "query_text": request.query,
            "status": "processing",
            "sources_requested": ["pubmed", "sukl"] # Default for now
        }
        res = supabase.table("queries").insert(query_data).execute()
        if res.data:
            query_id = res.data[0]["id"]
        
        # 2. Invoke AI Graph
        # Convert history
        messages = []
        if request.items:
            for msg in request.items:
                if msg.get("role") == "user":
                    messages.append(HumanMessage(content=msg.get("content", "")))
                elif msg.get("role") == "assistant":
                    messages.append(AIMessage(content=msg.get("content", "")))
        messages.append(HumanMessage(content=request.query))
        
        inputs = {"messages": messages}
        result = await graph_app.ainvoke(inputs)
        
        # Extract Results
        final_answer = result.get("final_answer", "")
        query_type = result.get("query_type", "unknown")
        
        # 3. Format Citations
        citations_list = []
        context = result.get("retrieved_context", [])
        
        for idx, item in enumerate(context, 1):
            source = item.get("source")
            data = item.get("data", {})
            
            # Map based on source
            cit = {
                "query_id": query_id,
                "citation_order": idx,
                "source_type": source if source in ['pubmed', 'sukl', 'guidelines'] else 'other',
                "title": data.get("title") or data.get("name") or "Unknown Title",
                "url": data.get("url") or data.get("spc_url"),
                "snippet": data.get("abstract") or data.get("description"),
            }
            
            # Specific fields
            if source == 'pubmed':
                cit["pmid"] = data.get("pmid")
                cit["doi"] = data.get("doi")
                # Authors is list in data, but text[] in DB
                if data.get("authors"):
                     cit["authors"] = data.get("authors")
            elif source == 'sukl':
                cit["external_id"] = data.get("sukl_code")
            
            citations_list.append(cit)
            
        # 4. Save Citations to DB
        if citations_list and query_id:
            supabase.table("citations").insert(citations_list).execute()
            
        # 5. Update Query Record (Completed)
        if query_id:
            supabase.table("queries").update({
                "response_text": final_answer,
                "status": "completed",
                "query_type": query_type if query_type in ['quick', 'deep'] else 'quick', # Simple mapping for now
                "completed_at": "now()",
                "sources_searched": list(set(c["source_type"] for c in citations_list))
            }).eq("id", query_id).execute()
            
        # Return Response
        frontend_citations = []
        for c in citations_list:
            frontend_citations.append({
                "source": c["source_type"],
                "title": c["title"],
                "url": c["url"],
                "metadata": c 
            })

        return QueryResponse(
            response=final_answer,
            query_type=query_type,
            citations=frontend_citations
        )
        
    except Exception as e:
        # Mark as failed if we created the record
        if query_id:
             supabase.table("queries").update({
                "status": "failed",
                "completed_at": "now()"
            }).eq("id", query_id).execute()
            
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream")
async def chat_stream_endpoint(body: StreamRequest):
    """
    Streaming chat endpoint. Returns NDJSON chunks.
    Format: {"type": "token", "content": "..."} or {"type": "metadata", "data": {...}}
    """
    logger.info("Received chat stream request")
    
    async def event_generator():
        try:
            from backend.agent_graph import app as agent_app
            
            inputs = {"messages": [HumanMessage(content=body.message)]}
            citations = []
            
            # Save user message if session_id provided  
            if body.session_id:
                await history_service.add_message(
                    session_id=body.session_id,
                    role="user",
                    content=body.message
                )

            # Use astream_events to catch tool calls and tokens
            accumulated_content = ""
            async for event in agent_app.astream_events(inputs, version="v1"):
                kind = event["event"]
                
                if kind == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        if isinstance(content, str):
                            accumulated_content += content
                            yield json.dumps({"type": "token", "content": content}) + "\n"
                        elif isinstance(content, list):
                            for block in content:
                                if isinstance(block, str):
                                    accumulated_content += block
                                    yield json.dumps({"type": "token", "content": block}) + "\n"
                        else:
                             chunk_str = str(content)
                             accumulated_content += chunk_str
                             yield json.dumps({"type": "token", "content": chunk_str}) + "\n"
                
                elif kind == "on_tool_end":
                    if event["name"] == "search_sukl_drugs":
                        try:
                            output_str = str(event["data"].get("output", ""))
                            urls = re.findall(r'https://www\.sukl\.cz/modules/medication/detail\.php\S+', output_str)
                            if urls:
                                url = urls[0]
                            else:
                                codes = re.findall(r'SÚKL:\s*([0-9]+)', output_str)
                                if codes:
                                    code = codes[0]
                                    url = f"https://www.sukl.cz/modules/medication/detail.php?code={code}&tab=info"
                                else:
                                    url = "https://www.sukl.cz/modules/medication/search.php"
                        except Exception as e:
                             logger.error("Error extracting SÚKL URL", error=e)
                             url = "https://www.sukl.cz/modules/medication/search.php"

                        citations.append({
                            "id": "sukl-db",
                            "type": "database", 
                            "value": "sukl",
                            "title": "Databáze léků SÚKL (2025)",
                            "year": 2025,
                            "url": url
                        })

            # Send metadata
            suggestions = []
            if citations:
                suggestions = ["Jaké je dávkování?", "Existují nějaké interakce?", "Jaká je cena?"]
            
            metadata = {
                "citations": citations,
                "suggestions": suggestions
            }
            yield json.dumps({"type": "metadata", "data": metadata}) + "\n"

            # Save assistant response
            if body.session_id:
                await history_service.add_message(
                    session_id=body.session_id,
                    role="assistant",
                    content=accumulated_content,
                    citations=citations
                )

        except Exception as e:
            logger.error("Error in stream", error=e)
            yield json.dumps({"type": "error", "content": str(e)}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")

@router.get("/history", response_model=List[Dict[str, Any]])
async def get_history(
    current_user: Dict[str, Any] = Depends(get_current_user),
    limit: int = 20,
    offset: int = 0
):
    supabase = get_supabase_client()
    try:
        res = supabase.table("queries")\
            .select("id, query_text, response_text, created_at, status, query_type")\
            .eq("user_id", current_user["id"])\
            .order("created_at", desc=True)\
            .limit(limit)\
            .range(offset, offset + limit - 1)\
            .execute()
            
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
