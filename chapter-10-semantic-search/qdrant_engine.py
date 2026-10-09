"""The same engine on Qdrant, with a filter on metadata (Listing 10.6).

Uses the Qdrant client's in-memory mode: no server to install. For a real
instance, just replace ":memory:" with the service address.

Imports the already indexed engine from semantic_search_engine.py: on
import the embedding model is loaded and the corpus is encoded.
"""

from qdrant_client import QdrantClient, models

from semantic_search_engine import engine

client = QdrantClient(":memory:")   # or url="http://..."

client.create_collection(
    collection_name="support",
    vectors_config=models.VectorParams(
        size=384, distance=models.Distance.DOT),
)
client.upsert(
    collection_name="support",
    points=[models.PointStruct(
                id=i,
                vector=engine.M[i].tolist(),
                payload={"chunk_id": c["id"], "topic": c["topic"]})
            for i, c in enumerate(engine.chunks)],
)

q = engine.model.encode("the laptop won't turn on",
                        normalize_embeddings=True)
response = client.query_points(
    collection_name="support",
    query=q.tolist(),
    query_filter=models.Filter(must=[
        models.FieldCondition(key="topic",
            match=models.MatchValue(value="hardware"))]),
    limit=3,
)
for p in response.points:
    print(p.payload["chunk_id"], round(p.score, 2))
