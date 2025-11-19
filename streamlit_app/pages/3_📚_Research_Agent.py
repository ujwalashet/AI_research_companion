import streamlit as st
import requests

st.title("📚 Research Generator")

topic = st.text_input("Enter your research topic")

if st.button("Generate Research"):
    response = requests.post("http://127.0.0.1:8000/research", data={"topic": topic})
    
    st.subheader("📌 Summary")
    st.write(response.json()["summary"])
    
    st.subheader("📝 Quiz")
    st.write(response.json()["quiz"])
