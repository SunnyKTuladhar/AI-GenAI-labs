import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)


def create_collection(collection_name: str, vector_size: int):
    # Skip if it already exists, so re-running the indexing doesn't crash
    if client.collection_exists(collection_name):
        return

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE,
        ),
    )


def store_embeddings(embedded_chunks: list[dict]):
    points = []

    for idx, chunk in enumerate(embedded_chunks):
        points.append(
            PointStruct(
                id=idx,
                vector=chunk["embedding"],
                payload={"content": chunk["content"], "source": chunk["source"]},
            )
        )

    client.upsert(collection_name="uniassist", points=points)
