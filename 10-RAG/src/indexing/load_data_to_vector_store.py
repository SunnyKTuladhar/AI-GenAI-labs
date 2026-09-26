from src.indexing.loader import load_document
from  src.indexing.chunker import chunk_document
from src.indexing.embed import embed_chunks
from src.indexing.vector_store import store_embeddings,create_collection

docuemnt =load_document("data")  # run from the project folder
chunks = chunk_document(documents=docuemnt)
embeded_chunks = embed_chunks(chunks=chunks)
create_collection("uniassist",384)
store_embeddings(embedded_chunks=embeded_chunks)
print("store completed" )