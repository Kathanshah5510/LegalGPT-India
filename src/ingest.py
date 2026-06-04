from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import os


def extract_text(pdf_path):
    """
    Extract text from all pages of a PDF.
    """

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def chunk_text(text, chunk_size=1000, overlap=200):
    """
    Split text into overlapping chunks.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


def main():

    pdf_path = "D:\\MTech\\Projects\\LegalGPT-India\\data\\constitution.pdf"

    print("=" * 50)
    print("Reading PDF...")
    print("=" * 50)

    reader = PdfReader(pdf_path)

    print(f"Pages: {len(reader.pages)}")

    text = extract_text(pdf_path)

    print(f"\nTotal characters extracted: {len(text):,}")

    print("\nFirst 2000 characters:\n")
    print(text[:2000])

    print("\n" + "=" * 50)
    print("Chunking Text...")
    print("=" * 50)

    chunks = chunk_text(
        text=text,
        chunk_size=1000,
        overlap=200
    )

    print(f"Total chunks: {len(chunks)}")

    print("\nChunk length samples:")
    print(f"Chunk 0   : {len(chunks[0])}")
    print(f"Chunk 1   : {len(chunks[1])}")
    print(f"Chunk 100 : {len(chunks[100])}")

    print("\nFirst chunk:\n")
    print(chunks[0])

    print("\n" + "=" * 50)
    print("Loading Embedding Model...")
    print("=" * 50)

    model = SentenceTransformer(
        "BAAI/bge-small-en-v1.5",
        device="cuda"
    )

    print("\nGenerating embeddings...")

    embeddings = model.encode(
        chunks,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    print("\nEmbedding Shape:")
    print(embeddings.shape)

    print("\n" + "=" * 50)
    print("Saving Data...")
    print("=" * 50)

    os.makedirs("D:\\MTech\\Projects\\LegalGPT-India\\vector_db", exist_ok=True)

    np.save(
        "D:\\MTech\\Projects\\LegalGPT-India\\vector_db\\chunk_embeddings.npy",
        embeddings
    )

    with open(
        "D:\\MTech\\Projects\\LegalGPT-India\\vector_db\\chunks.pkl",
        "wb"
    ) as f:
        pickle.dump(chunks, f)

    print("\nSaved:")
    print("vector_db/chunk_embeddings.npy")
    print("vector_db/chunks.pkl")

    print("\nPipeline completed successfully!")


if __name__ == "__main__":
    main()