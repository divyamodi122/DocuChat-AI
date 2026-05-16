import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()


def extract_text_from_pdfs(pdf_files) -> str:
    """Extract text from one or multiple PDF files."""
    full_text = ""
    for pdf in pdf_files:
        try:
            reader = PyPDF2.PdfReader(pdf)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
        except Exception as e:
            print(f"[pdf_processor] Error reading PDF: {e}")
    return full_text


def split_text_into_chunks(text: str):
    """Split large text into smaller chunks for vector storage."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = splitter.split_text(text)
    return chunks


def create_vector_store(chunks: list):
    """Create FAISS vector store from text chunks using Gemini embeddings."""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=("AIzaSyBALczuKV3E7-24HNhdq8-i2ZZC2YvmFRQ")
    )
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    return vector_store


def process_pdfs(pdf_files):
    """Full pipeline: PDF → text → chunks → vector store."""
    text = extract_text_from_pdfs(pdf_files)
    if not text.strip():
        raise ValueError("Could not extract text from PDF. Make sure it's not a scanned image.")
    chunks = split_text_into_chunks(text)
    vector_store = create_vector_store(chunks)
    return vector_store, len(chunks)