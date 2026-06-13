import os
import re
import pickle
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def split_into_articles(text):
    # Improved regex to catch articles like 21, 21A, 371J etc.
    pattern = r'\n(?=\d+[A-Z]?\.\s)'
    articles = re.split(pattern, text)
    cleaned_articles = [art.strip() for art in articles if art.strip()]
    return cleaned_articles

def main():
    pdf_path = os.path.join(BASE_DIR, "data", "constitution.pdf")
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found. Please place the Constitution PDF in the data folder.")
        return

    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    
    print("Splitting text into articles...")
    articles = split_into_articles(text)
    print(f"Total articles found: {len(articles)}")

    # Load embedding model
    print("Loading embedding model...")
    model = SentenceTransformer('BAAI/bge-small-en-v1.5')

    print("Generating embeddings for articles...")
    article_embeddings = []
    for article in tqdm(articles):
        embedding = model.encode("Represent this sentence for searching relevant passages: " + article)
        article_embeddings.append(embedding)
    
    article_embeddings = np.array(article_embeddings)

    # Save embeddings and articles
    db_dir = os.path.join(BASE_DIR, "vector_db")
    os.makedirs(db_dir, exist_ok=True)
    
    np.save(os.path.join(db_dir, "article_embeddings.npy"), article_embeddings)
    with open(os.path.join(db_dir, "articles.pkl"), "wb") as f:
        pickle.dump(articles, f)
    
    print(f"Ingestion complete. Saved to {db_dir}")

if __name__ == "__main__":
    main()
