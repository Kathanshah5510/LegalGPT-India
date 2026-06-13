<!-- # LegalGPT-India

An AI-powered legal assistant built using Retrieval-Augmented Generation (RAG).

## Features (Planned)

- PDF ingestion
- Semantic search using embeddings
- FAISS vector database
- Gemini-powered legal Q&A
- Streamlit web interface
- Source citations

## Current Progress

- [x] Project setup
- [x] Constitution PDF ingestion
- [x] Text extraction
- [x] Chunking
- [x] Embeddings
- [ ] FAISS indexing
- [ ] Retrieval pipeline
- [ ] Gemini integration
- [ ] Streamlit UI -->


# LegalGPT-India ⚖️

A Retrieval-Augmented Generation (RAG) chatbot built to answer queries about the **Constitution of India**. This project uses article-based chunking for better semantic retrieval and Google Gemini for generating accurate legal responses.

## Features
- **Article-Based Chunking**: Splits the Constitution by legal structure (Article 14, 15, 21, etc.) instead of random character windows.
- **Semantic Search**: Uses `BAAI/bge-small-en-v1.5` embeddings for high-quality retrieval.
- **LLM Integration**: Powered by Google Gemini (Gemini 1.5 Flash) for intelligent responses.
- **Streamlit UI**: A clean, interactive web interface for chatting with the legal assistant.

## Project Structure
```text
LegalGPT-India/
│
├── data/
│   └── constitution.pdf      # Place the PDF here
│
├── src/
│   ├── ingest_articles.py    # Extracts and embeds articles
│   ├── retrieve_articles.py  # Retrieval logic
│   └── chatbot.py            # Gemini integration
│
├── vector_db/                # Created after running ingest
│   ├── article_embeddings.npy
│   └── articles.pkl
│
├── app.py                    # Streamlit application
├── requirements.txt          # Dependencies
└── README.md
```

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- A Google Gemini API Key (Get it from [Google AI Studio](https://aistudio.google.com/app/apikey))

### 2. Installation
Clone this project and install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Data Preparation
Place the `constitution.pdf` file in the `data/` folder.

### 4. Ingestion
Run the ingestion script to process the PDF and create the vector database:
```bash
cd src
python ingest_articles.py
```

### 5. Run the App
Launch the Streamlit interface:
```bash
streamlit run app.py
```

## How it Works
1. **Extraction**: `ingest_articles.py` uses regex to identify and split the PDF into individual articles (e.g., Article 21, Article 21A).
2. **Embedding**: Each article is converted into a vector embedding using the BGE model.
3. **Retrieval**: When you ask a question, the system finds the top 3 most relevant articles using cosine similarity.
4. **Generation**: The retrieved articles are passed as context to Google Gemini, which generates a professional legal response.
5. **UI**: The response is displayed in the Streamlit app, along with citations to the relevant articles.
