import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


print("=" * 50)
print("Loading Data...")
print("=" * 50)

embeddings = np.load("D:\\MTech\\Projects\\LegalGPT-India\\vector_db\\chunk_embeddings.npy")

with open("D:\\MTech\\Projects\\LegalGPT-India\\vector_db\\chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

print(f"Embeddings Shape: {embeddings.shape}")
print(f"Chunks Loaded: {len(chunks)}")

print("\nLoading Embedding Model...")

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5",
    device="cpu"
)

while True:

    query = input("\nAsk a legal question (or type exit): ")

    if query.lower() == "exit":
        break

    # query_embedding = model.encode([query])
    query_embedding = model.encode(["Represent this sentence for searching relevant passages: " + query])

    similarities = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    top_k = 10

    top_indices = similarities.argsort()[-top_k:][::-1]

    print("\n" + "=" * 50)
    print("TOP MATCHES")
    print("=" * 50)

    for rank, idx in enumerate(top_indices, start=1):

        print(f"\nRank {rank}")
        print(f"Similarity: {similarities[idx]:.4f}")
        print("-" * 50)

        print(chunks[idx][:800])

        print("\n")