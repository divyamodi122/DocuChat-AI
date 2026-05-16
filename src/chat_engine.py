from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()


def create_chat_engine(vector_store):
    """Create chat engine using Gemini + FAISS retriever."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",
        google_api_key=("AIzaSyBALczuKV3E7-24HNhdq8-i2ZZC2YvmFRQ"),
        temperature=0.3,
    )
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )
    return {"llm": llm, "retriever": retriever}


def get_answer(chain: dict, question: str, chat_history: list = None) -> dict:
    """Get answer from Gemini using retrieved context."""
    try:
        llm = chain["llm"]
        retriever = chain["retriever"]

        
        docs = retriever.invoke(question)
        context = "\n\n".join([doc.page_content for doc in docs])

        
        system_prompt = f"""You are DocuChat — a helpful AI assistant that answers questions based on uploaded PDF documents.

Use the context below to answer the question. If the answer is not in the context,
say "I couldn't find that information in the uploaded document."
Don't make up answers. Be concise and helpful. Use bullet points where appropriate.

Context:
{context}"""

        messages = [{"role": "system", "content": system_prompt}]

        
        if chat_history:
            for msg in chat_history[-6:]:
                messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": question})

        response = llm.invoke(messages)

        return {
            "answer": response.content,
            "source_docs": docs
        }
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "source_docs": []
        }