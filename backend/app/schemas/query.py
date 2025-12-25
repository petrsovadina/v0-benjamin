from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any

class QueryRequest(BaseModel):
    items: Optional[List[Dict[str, str]]] = Field(default=[], alias="history")
    query: Optional[str] = Field(default=None, alias="message")
    
    # Allow passing 'query' and 'items' directly as well if needed, 
    # but Pydantic V2 alias_generator might be cleaner. 
    # For now, let's just make query optional and validate that one acts as the main content.

    @validator("query", pre=True, always=True)
    def check_query_or_message(cls, v, values):
        # If 'query' was not set by alias 'message', maybe it was passed as 'query'?
        # Pydantic usually handles alias OR field name if allow_population_by_field_name is True.
        return v
        
    class Config:
        populate_by_name = True

class QueryResponse(BaseModel):
    response: str
    query_type: Optional[str] = None
    citations: Optional[List[Dict[str, Any]]] = []
    status: str = "success"
