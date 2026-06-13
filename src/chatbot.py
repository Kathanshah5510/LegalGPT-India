import os
import google.generativeai as genai
from .retrieve_articles import retrieve

class LegalChatbot:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = self._setup_model()
        self.chat = self.model.start_chat(history=[])
        self.history = [] # To keep track of conversation for query rewriting

    def _setup_model(self):
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        priority = [
            'models/gemini-1.5-flash-latest',
            'models/gemini-1.5-flash',
            'models/gemini-1.5-pro-latest',
            'models/gemini-1.5-pro',
            'models/gemini-pro'
        ]
        for model_path in priority:
            if model_path in available_models:
                return genai.GenerativeModel(model_path)
        if available_models:
            return genai.GenerativeModel(available_models[0])
        raise Exception("No supported Gemini models found in your account.")

    def rewrite_query(self, user_query):
        """Rewrites the user query based on conversation history for better retrieval."""
        if not self.history:
            return user_query
            
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in self.history[-3:]])
        prompt = f"""
Given the following conversation history and a new user query, rewrite the user query to be a standalone search query that can be used to retrieve relevant legal articles from the Constitution of India.
Do not answer the query, just return the rewritten search query.

Conversation History:
{history_text}

New User Query: {user_query}

Standalone Search Query:"""
        
        try:
            response = self.model.generate_content(prompt)
            rewritten = response.text.strip()
            return rewritten if rewritten else user_query
        except:
            return user_query

    def get_response(self, query):
        # 1. Rewrite query for better RAG if there's history
        search_query = self.rewrite_query(query)
        
        # 2. Retrieve relevant legal articles using the rewritten query
        retrieved_docs = retrieve(search_query, top_k=3)
        
        if isinstance(retrieved_docs, str):
            return retrieved_docs, []

        context = "\n\n".join([doc['article'] for doc in retrieved_docs])
        
        # 3. Construct prompt with context
        prompt = f"""
You are an expert Indian Legal Assistant. Use the following retrieved articles from the Constitution of India to answer the user's query accurately.
If the information is not in the context, state that you don't have enough information but provide general legal guidance.

Retrieved Context:
{context}

User Query: {query}

Answer:
"""
        # 4. Generate response using chat history
        try:
            response = self.chat.send_message(prompt)
            # Update internal history for query rewriting
            self.history.append({"role": "user", "content": query})
            self.history.append({"role": "assistant", "content": response.text})
            return response.text, retrieved_docs
        except Exception as e:
            return f"Error generating response: {str(e)}", retrieved_docs
