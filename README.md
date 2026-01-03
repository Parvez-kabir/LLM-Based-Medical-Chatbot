📌 Project Overview

This project presents an LLM-based Law Chatbot built using the Retrieval-Augmented Generation (RAG) framework and Google Gemini Pro.
The system is designed to provide accurate, context-aware, and document-grounded legal responses by retrieving relevant information from a legal knowledge base before generating answers.

Unlike traditional chatbots, this solution minimizes hallucination by grounding responses in verified legal documents, making it suitable for law-related Q&A, academic research, and legal assistance prototypes.

User Interface 
<img width="849" height="963" alt="image" src="https://github.com/user-attachments/assets/5e802fa5-aba0-472b-aed1-6070139fdc10" />

<img width="863" height="963" alt="image" src="https://github.com/user-attachments/assets/56afdb4c-d09f-4168-86bd-37e242f83d59" />



⚙️ Key Features

🔍 Retrieval-Augmented Generation (RAG) architecture

🤖 Powered by Google Gemini Pro LLM

📚 Legal document ingestion and vector-based semantic search

🧠 Context-aware and source-grounded responses

⚡ Reduced hallucination compared to vanilla LLM chatbots

🧩 Modular and extensible design



🏗️ System Architecture

Document Loader – Loads and preprocesses legal documents (PDF / text)

Text Chunking – Splits documents into manageable semantic chunks

Embedding Model – Converts text chunks into vector embeddings

Vector Database – Stores embeddings for efficient similarity search

Retriever – Fetches relevant legal context based on user query

Gemini Pro LLM – Generates answers using retrieved context



🛠️ Tech Stack

LLM: Google Gemini Pro

Vector Store: Pinecone

Language: Python

Embedding Model: Google / HuggingFace Embeddings

Environment: VS Code
