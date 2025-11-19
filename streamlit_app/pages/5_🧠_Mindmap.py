import streamlit as st
import requests

st.title("🧠 Mindmap Generator")

text = st.text_area("Enter text")

if st.button("Generate Mindmap"):
    response = requests.post("http://127.0.0.1:8000/generate_mindmap", data={"text": text})

    st.code(response.json()["mindmap"])
