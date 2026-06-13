import os
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def retrieve(query, top_k=3):
    db_dir = os.path.join(BASE_DIR, "vector_db")
    embeddings_path = os.path.join(db_dir, "article_embeddings.npy")
    articles_path = os.path.join(db_dir, "articles.pkl")

    try:
        embeddings = np.load(embeddings_path)
        with open(articles_path, "rb") as f:
            articles = pickle.load(f)
    except FileNotFoundError:
        return "⚠️ Error: Vector database not found. Please run `python src/ingest_articles.py` to generate it."

    model = SentenceTransformer('BAAI/bge-small-en-v1.5')
    query_embedding = model.encode(["Represent this sentence for searching relevant passages: " + query])
    
    similarities = cosine_similarity(query_embedding, embeddings).flatten()
    top_indices = similarities.argsort()[-top_k:][::-1]
    
    results = []
    for idx in top_indices:
        results.append({
            "article": articles[idx],
            "score": similarities[idx]
        })
    return results

if __name__ == "__main__":
    query = input("Enter your legal query: ")
    results = retrieve(query)
    if isinstance(results, str):
        print(results)
    else:
        for i, res in enumerate(results):
            print(f"\nRank {i+1} (Score: {res['score']:.4f}):")
            print("-" * 30)
            print(res['article'][:500] + "..." if len(res['article']) > 500 else res['article'])
