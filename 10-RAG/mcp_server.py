"""UniAssist MCP server — our RAG retrieval, exposed as an MCP tool.

We are NOT rewriting the RAG. We just import the functions we already built
and wrap them with @mcp.tool so any MCP client (Claude Desktop, our own agent)
can use them.

The tool only does retrieval (embed -> Qdrant -> rerank) and returns the raw
policy text. The client's own LLM reads that text and writes the answer.

Test in the inspector:   uv run fastmcp dev inspector mcp_server.py
"""

from dotenv import load_dotenv
from fastmcp import FastMCP

# Load .env BEFORE importing our RAG modules: they download models and connect
# to Qdrant at import time, so settings like SSL_CERT_FILE must be set first.
load_dotenv()

from src.retrival.query_embedder import embed_query
from src.retrival.reranker import reranker
from src.retrival.retriver import retrieve

# Create the server — just give it a name
mcp = FastMCP("UniAssist")


# The docstring is important: the AI reads it to decide WHEN to use this tool.


@mcp.tool
def search_policies(query: str) -> str:
    """Search the university policy documents (attendance, grading, graduation,
    admissions, exams, makeup exams, library, leave, scholarships, student ID).
    Returns the most relevant policy text with its source file."""

    # 1. Turn the question into a vector
    query_vector = embed_query(query)

    # 2. Get 10 candidate chunks from Qdrant
    candidates = retrieve(query_vector=query_vector, top_k=10)

    # 3. Keep the best 3 using the reranker
    best_chunks = reranker(query=query, results=candidates, top_k=3)

    # 4. Return the text + where it came from
    texts = []
    for chunk, score in best_chunks:
        source = chunk.payload["source"]
        content = chunk.payload["content"]
        texts.append(f"[source: {source}]\n{content}")

    return "\n\n".join(texts)


if __name__ == "__main__":
    mcp.run()
