# DocuChat AI — Chat with Any PDF

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green)
![Gemini](https://img.shields.io/badge/Google_Gemini-AI-orange)
![RAG](https://img.shields.io/badge/RAG-Architecture-purple)

> **Upload any PDF and have a conversation with it using AI.**  
> DocuChat uses Retrieval Augmented Generation (RAG) to understand your documents and answer questions accurately.


# Live Demo
> Coming soon (Streamlit Cloud deployment)


# How It Works

```
 Upload PDF  →   Chunk Text  →   Create Embeddings  →   Store in FAISS
                                                                      ↓
 Ask Question  →   Retrieve Context  →   Gemini Answers  →   Response
```

1. **PDF Processing** — PyPDF2 extracts text from uploaded PDF
2. **Chunking** — LangChain splits text into 1000-token chunks with 200-token overlap
3. **Embeddings** — Google Gemini Embeddings convert chunks to vectors
4. **Vector Store** — FAISS stores and indexes all vectors locally
5. **Retrieval** — Top 4 most relevant chunks retrieved per question
6. **Generation** — Gemini LLM generates accurate answers from retrieved context

# Features

-  Upload one or multiple PDF files
-  Multi-turn conversation with memory
-  RAG architecture for accurate, grounded answers
-  Fast retrieval using FAISS vector store
-  Clean chat UI with message history
-  Supports any PDF — research papers, textbooks, reports, contracts

#  Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| LLM | Google Gemini 2.0 Flash |
| Embeddings | Google Gemini Embeddings |
| RAG Framework | LangChain |
| Vector Store | FAISS (Facebook AI) |
| PDF Processing | PyPDF2 |
| Environment | python-dotenv |

# Project Structure

```
DocuChat-AI/
├── app.py                  # Streamlit chat dashboard
├── requirements.txt        # Dependencies
├── .env                    # API keys (not pushed to GitHub)
├── src/
│   ├── pdf_processor.py    # PDF parsing + chunking + vector store
│   └── chat_engine.py      # Gemini LLM + RAG retrieval chain
└── README.md
```
# Setup & Run Locally
# 1. Clone the repo
git clone https://github.com/divyamodi122/DocuChat-AI.git
cd DocuChat-AI

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Gemini API key
# Create a .env file and add:
# GOOGLE_API_KEY=your_gemini_api_key_here

# 5. Run the app
streamlit run app.py

# Get Free Gemini API Key

1. Go to **aistudio.google.com**
2. Click **Get API Key** → **Create API Key**
3. Copy and paste into `.env` file

#  Skills Showcased

`Generative AI` `RAG Architecture` `LangChain` `FAISS Vector DB` `Google Gemini` `Embeddings` `Python` `Streamlit` `PDF Processing` `Prompt Engineering`

# Contact

**Divya Modi** — [LinkedIn](https://linkedin.com) | [GitHub](https://github.com/divyamodi122)