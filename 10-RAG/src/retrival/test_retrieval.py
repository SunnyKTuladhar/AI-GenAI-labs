from src.retrival.query_embedder import embed_query
from src.retrival.retriver  import retrieve
from src.retrival.reranker import reranker

query  = "what is the exam policy?"

#embed the query 
embedding = embed_query(query=query)
print("Query embedded")
print("Vector dimension:", len(embedding))

#retive candidate form the Qdrant 
results = retrieve(embedding,top_k=10)
print("\nQdrant results:")
print("Number of candidates:", len(results))


#Reranker 
reranker_result = reranker(
    query=query,
    results=results,
    top_k=3
)
print("\n\n========== RERANKED RESULTS ==========")


for result, score in reranker_result:
    print("\nReranker score:", score)
    print("Original Qdrant score:", result.score)
    print("Source:", result.payload["source"])
    print("Content:", result.payload["content"][:200])
