import streamlit as st
import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pdf_processor import process_pdfs
from chat_engine import create_chat_engine, get_answer

# ─── Page Config ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="DocuChat — Chat with your PDF",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)



st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0 0.2rem 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .chat-message-user {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 0.95rem;
    }
    .chat-message-bot {
        background: #f3f4f6;
        color: #1f2937;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 80%;
        font-size: 0.95rem;
        border-left: 3px solid #4f46e5;
    }
    .status-box {
        background: #ecfdf5;
        border: 1px solid #6ee7b7;
        border-radius: 8px;
        padding: 10px 16px;
        color: #065f46;
        font-weight: 500;
    }
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #4f46e5;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)



if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chain" not in st.session_state:
    st.session_state.chain = None

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

if "pdf_names" not in st.session_state:
    st.session_state.pdf_names = []



with st.sidebar:
    st.markdown("##  Upload Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more PDF files to chat with"
    )

    if uploaded_files:
        st.markdown(f"**{len(uploaded_files)} file(s) selected:**")
        for f in uploaded_files:
            st.markdown(f"• {f.name}")

    process_btn = st.button(" Process PDFs", use_container_width=True, type="primary")

    if process_btn:
        if not uploaded_files:
            st.error("Please upload at least one PDF!")
        else:
            with st.spinner(" Processing PDFs... building vector store..."):
                try:
                    vector_store, num_chunks = process_pdfs(uploaded_files)
                    st.session_state.chain = create_chat_engine(vector_store)
                    st.session_state.pdf_processed = True
                    st.session_state.pdf_names = [f.name for f in uploaded_files]
                    st.session_state.chat_history = []
                    st.success(f" Done! {num_chunks} chunks indexed.")
                except Exception as e:
                    st.error(f" Error: {str(e)}")

    st.markdown("---")

    if st.session_state.pdf_processed:
        st.markdown('<div class="status-box"> Ready to chat!</div>', unsafe_allow_html=True)
        st.markdown(f"**Documents loaded:**")
        for name in st.session_state.pdf_names:
            st.markdown(f" {name}")

    st.markdown("---")
    st.markdown("###  Sample Questions")
    st.markdown("""
    - What is this document about?
    - Summarize the key points
    - What are the main conclusions?
    - Explain [specific topic] from the document
    """)

    if st.button(" Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()



st.markdown('<h1 class="main-header" DocuChat</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload any PDF and chat with it using AI — Powered by Gemini + RAG</p>', unsafe_allow_html=True)


chat_container = st.container()

with chat_container:
    if not st.session_state.pdf_processed:
        st.info(" Upload a PDF from the sidebar and click **Process PDFs** to start chatting!")

        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("###  Smart Search")
            st.markdown("Uses RAG to find the most relevant parts of your document before answering.")
        with c2:
            st.markdown("###  AI Powered")
            st.markdown("Powered by Google Gemini 1.5 Flash — fast, accurate, and free.")
        with c3:
            st.markdown("###  Multi-turn Chat")
            st.markdown("Remembers conversation history for follow-up questions.")

    else:
        
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(
                    f'<div class="chat-message-user"> {message["content"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="chat-message-bot"> {message["content"]}</div>',
                    unsafe_allow_html=True
                )



if st.session_state.pdf_processed:
    st.markdown("---")
    col1, col2 = st.columns([5, 1])

    with col1:
        user_question = st.text_input(
            "Ask anything about your document...",
            placeholder="e.g. What is the main topic of this document?",
            label_visibility="collapsed"
        )
    with col2:
        ask_btn = st.button("Ask ", use_container_width=True, type="primary")

    if ask_btn and user_question.strip():
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })

        with st.spinner(" Thinking..."):
            response = get_answer(st.session_state.chain, user_question, st.session_state.chat_history)
            answer = response["answer"]

        
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()