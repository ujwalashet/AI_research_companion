import streamlit as st
import requests

st.title("🤖 RAG Chat Assistant")

question = st.text_input("Ask something based on your uploaded documents:")

if st.button("Ask"):
    response = requests.get("http://127.0.0.1:8000/rag_chat", params={"question": question})

    st.markdown(f"<div class='bot-message'>{response.json()['answer']}</div>", unsafe_allow_html=True)
