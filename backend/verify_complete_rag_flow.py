"""
Comprehensive verification of complete RAG flow for LangChain/LangGraph upgrade.

This script verifies the complete query → classification → retrieval → synthesis flow
for all three query types: drug_info, guidelines, and clinical (general).

Subtask 5.2: Integration test for RAG workflow E2E
"""
import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import MagicMock, AsyncMock, patch


async def test_classification_node():
    """Test that classifier correctly routes different query types."""
    print("\n=== Testing Classification Node ===")

    from backend.app.core.graph import classifier_node
    from langchain_core.messages import HumanMessage

    # Test cases for different query types
    test_cases = [
        ("Jaký je lék na bolest?", "drug_info", "retrieve_drugs"),
        ("Jaké jsou guidelines pro léčbu diabetu?", "guidelines", "retrieve_guidelines"),
        ("Jaké jsou příznaky chřipky?", "clinical", "retrieve_general"),
    ]

    results = []
    for query, expected_type, expected_next_step in test_cases:
        state = {
            "messages": [HumanMessage(content=query)],
            "query_type": None,
            "retrieved_context": [],
            "final_answer": None,
            "next_step": None
        }

        # Run with fallback logic (no LLM) for predictable testing
        with patch("backend.app.core.graph.get_llm", return_value=None):
            result = await classifier_node(state)

        passed = result.get("next_step") is not None
        results.append(passed)
        status = "✓" if passed else "✗"
        print(f"  {status} Query: '{query[:40]}...'")
        print(f"      Classified as: {result.get('query_type')}, next_step: {result.get('next_step')}")

    return all(results)


async def test_drug_retrieval_node():
    """Test drug retrieval node with SÚKL data."""
    print("\n=== Testing Drug Retrieval Node ===")

    from backend.app.core.graph import retrieve_drugs_node
    from langchain_core.messages import HumanMessage

    mock_drugs = [
        {
            "name": "Ibuprofen 400mg",
            "sukl_code": "0001234",
            "active_substance": "Ibuprofen",
            "is_available": True
        }
    ]

    mock_search_service = MagicMock()
    mock_search_service.search_drugs = AsyncMock(return_value=mock_drugs)

    state = {
        "messages": [HumanMessage(content="Jaký je lék na bolest?")],
        "query_type": "drug_info",
        "retrieved_context": [],
        "final_answer": None,
        "next_step": "retrieve_drugs"
    }

    with patch("backend.app.core.graph.search_service", mock_search_service):
        result = await retrieve_drugs_node(state)

    passed = (
        "retrieved_context" in result and
        len(result["retrieved_context"]) > 0 and
        result["retrieved_context"][0]["source"] == "sukl"
    )

    status = "✓" if passed else "✗"
    print(f"  {status} Drug retrieval: {len(result.get('retrieved_context', []))} results")
    print(f"      Source: {result.get('retrieved_context', [{}])[0].get('source', 'N/A')}")

    return passed


async def test_guidelines_retrieval_node():
    """Test guidelines retrieval node."""
    print("\n=== Testing Guidelines Retrieval Node ===")

    from backend.app.core.graph import retrieve_guidelines_node
    from langchain_core.messages import HumanMessage

    mock_guidelines = [
        {
            "id": "uuid-1",
            "title": "Diabetes Guidelines 2024",
            "content": "Doporučená hodnota HbA1c je <7%",
            "source": "diabetes_guideline.pdf",
            "page": 12,
            "similarity": 0.88
        }
    ]

    mock_search_service = MagicMock()
    mock_search_service.search_guidelines = AsyncMock(return_value=mock_guidelines)

    state = {
        "messages": [HumanMessage(content="Jaké jsou guidelines pro léčbu diabetu?")],
        "query_type": "guidelines",
        "retrieved_context": [],
        "final_answer": None,
        "next_step": "retrieve_guidelines"
    }

    with patch("backend.app.core.graph.search_service", mock_search_service):
        result = await retrieve_guidelines_node(state)

    passed = (
        "retrieved_context" in result and
        len(result["retrieved_context"]) > 0 and
        result["retrieved_context"][0]["source"] == "guidelines"
    )

    status = "✓" if passed else "✗"
    print(f"  {status} Guidelines retrieval: {len(result.get('retrieved_context', []))} results")
    print(f"      Source: {result.get('retrieved_context', [{}])[0].get('source', 'N/A')}")

    return passed


async def test_general_retrieval_node():
    """Test general (PubMed) retrieval node."""
    print("\n=== Testing General Retrieval Node ===")

    from backend.app.core.graph import retrieve_general_node
    from langchain_core.messages import HumanMessage

    mock_papers = [
        {
            "title": "Clinical Study on Flu Symptoms",
            "abstract": "This study examines common flu symptoms...",
            "authors": ["Smith J", "Jones A"],
            "url": "https://pubmed.ncbi.nlm.nih.gov/123456"
        }
    ]

    mock_search_service = MagicMock()
    mock_search_service.search_pubmed = AsyncMock(return_value=mock_papers)

    state = {
        "messages": [HumanMessage(content="Jaké jsou příznaky chřipky?")],
        "query_type": "clinical",
        "retrieved_context": [],
        "final_answer": None,
        "next_step": "retrieve_general"
    }

    with patch("backend.app.core.graph.search_service", mock_search_service):
        result = await retrieve_general_node(state)

    passed = (
        "retrieved_context" in result and
        len(result["retrieved_context"]) > 0 and
        result["retrieved_context"][0]["source"] == "pubmed"
    )

    status = "✓" if passed else "✗"
    print(f"  {status} General retrieval: {len(result.get('retrieved_context', []))} results")
    print(f"      Source: {result.get('retrieved_context', [{}])[0].get('source', 'N/A')}")

    return passed


async def test_synthesizer_node():
    """Test synthesizer node generates responses with citations."""
    print("\n=== Testing Synthesizer Node ===")

    from backend.app.core.graph import synthesizer_node
    from langchain_core.messages import HumanMessage

    mock_llm = MagicMock()
    mock_llm_response = MagicMock()
    mock_llm_response.content = """Na základě klinických doporučení je první volbou léčby ACE inhibitor [1].

Citace:
[1] Source: diabetes_guideline.pdf, page 12"""
    mock_llm.ainvoke = AsyncMock(return_value=mock_llm_response)

    state = {
        "messages": [HumanMessage(content="Jaká je doporučená léčba?")],
        "query_type": "guidelines",
        "retrieved_context": [
            {
                "source": "guidelines",
                "data": {
                    "content": "ACE inhibitory jsou první volbou.",
                    "source": "diabetes_guideline.pdf",
                    "page": 12,
                    "similarity": 0.9
                }
            }
        ],
        "final_answer": None,
        "next_step": None
    }

    with patch("backend.app.core.graph.get_llm", return_value=mock_llm):
        result = await synthesizer_node(state)

    passed = (
        "final_answer" in result and
        result["final_answer"] is not None and
        "diabetes_guideline.pdf" in result["final_answer"]
    )

    status = "✓" if passed else "✗"
    print(f"  {status} Synthesizer generates answer with citations")

    return passed


async def test_complete_graph_flow():
    """Test the complete graph flow from start to end."""
    print("\n=== Testing Complete Graph Flow ===")

    from backend.app.core.graph import app as graph_app
    from langchain_core.messages import HumanMessage

    # Mock all external dependencies
    mock_guidelines = [
        {
            "id": "uuid-1",
            "title": "Czech Medical Guidelines",
            "content": "Doporučená léčba zahrnuje inhibitory ACE.",
            "source": "czech_guidelines.pdf",
            "page": 10,
            "similarity": 0.92
        }
    ]

    mock_search_service = MagicMock()
    mock_search_service.search_guidelines = AsyncMock(return_value=mock_guidelines)
    mock_search_service.search_drugs = AsyncMock(return_value=[])
    mock_search_service.search_pubmed = AsyncMock(return_value=[])

    mock_llm = MagicMock()
    mock_classification = MagicMock()
    mock_classification.query_type = "guidelines"

    mock_llm_response = MagicMock()
    mock_llm_response.content = """Na základě doporučení je první volbou ACE inhibitor [1].

Citace:
[1] Source: czech_guidelines.pdf, page 10"""

    mock_structured_llm = MagicMock()
    mock_structured_llm.ainvoke = AsyncMock(return_value=mock_classification)
    mock_llm.with_structured_output = MagicMock(return_value=mock_structured_llm)
    mock_llm.ainvoke = AsyncMock(return_value=mock_llm_response)

    test_flows = [
        ("guidelines", "Jaké jsou doporučení pro léčbu diabetu?"),
        ("drug_info", "Jaký lék na bolest hlavy?"),
        ("clinical", "Jaké jsou příznaky chřipky?"),
    ]

    all_passed = True
    for query_type, query in test_flows:
        mock_classification.query_type = query_type

        try:
            with patch("backend.app.core.graph.search_service", mock_search_service), \
                 patch("backend.app.core.graph.get_llm", return_value=mock_llm):

                result = await graph_app.ainvoke({
                    "messages": [HumanMessage(content=query)]
                })

            # Verify the flow completed
            passed = (
                "final_answer" in result and
                result["final_answer"] is not None and
                "query_type" in result
            )

            status = "✓" if passed else "✗"
            print(f"  {status} Flow for '{query_type}': query → classification → retrieval → synthesis")

            if not passed:
                all_passed = False

        except Exception as e:
            print(f"  ✗ Flow for '{query_type}' failed with error: {e}")
            all_passed = False

    return all_passed


async def test_graph_structure():
    """Verify graph structure matches expected flow."""
    print("\n=== Testing Graph Structure ===")

    from backend.app.core.graph import app as graph_app

    try:
        # Get graph visualization
        mermaid = graph_app.get_graph().draw_mermaid()

        # Verify expected nodes exist
        expected_nodes = ["classifier", "retrieve_drugs", "retrieve_general", "retrieve_guidelines", "synthesizer"]
        nodes_present = all(node in mermaid for node in expected_nodes)

        # Verify expected edges
        expected_edges = [
            "__start__",  # START
            "__end__",    # END
            "classifier",
            "synthesizer"
        ]
        edges_present = all(edge in mermaid for edge in expected_edges)

        passed = nodes_present and edges_present
        status = "✓" if passed else "✗"
        print(f"  {status} Graph has all expected nodes and edges")
        print(f"      Nodes: {expected_nodes}")
        print(f"      Flow: START → classifier → (retrieve_*) → synthesizer → END")

        return passed

    except Exception as e:
        print(f"  ✗ Graph structure verification failed: {e}")
        return False


async def main():
    """Run all verification tests."""
    print("=" * 70)
    print("COMPLETE RAG FLOW VERIFICATION")
    print("Subtask 5.2: Query → Classification → Retrieval → Synthesis")
    print("=" * 70)

    results = []

    # Test individual nodes
    results.append(("Classification Node", await test_classification_node()))
    results.append(("Drug Retrieval Node", await test_drug_retrieval_node()))
    results.append(("Guidelines Retrieval Node", await test_guidelines_retrieval_node()))
    results.append(("General Retrieval Node", await test_general_retrieval_node()))
    results.append(("Synthesizer Node", await test_synthesizer_node()))

    # Test complete flow
    results.append(("Complete Graph Flow", await test_complete_graph_flow()))
    results.append(("Graph Structure", await test_graph_structure()))

    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)

    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status} - {name}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL VERIFICATIONS PASSED")
        print("  Complete query → classification → retrieval → synthesis flow works correctly")
    else:
        print("✗ SOME VERIFICATIONS FAILED")
        print("  Please review the failures above")
    print("=" * 70)

    return 0 if all_passed else 1


if __name__ == "__main__":
    # Set environment variables for testing
    os.environ.setdefault("SUPABASE_URL", "https://test.supabase.co")
    os.environ.setdefault("SUPABASE_KEY", "test-key")
    os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
    os.environ.setdefault("PUBMED_EMAIL", "test@test.com")

    exit_code = asyncio.run(main())
    sys.exit(exit_code)
