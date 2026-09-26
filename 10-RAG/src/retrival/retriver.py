import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))

COLLECTION_NAME = "uniassist"


def retrieve(query_vector: list[float], top_k: int = 5):
    results = client.query_points(
        collection_name=COLLECTION_NAME, query=query_vector, limit=top_k
    )


    return results.points


