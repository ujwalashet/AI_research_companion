📚 AI RESEARCH COMPANION

A multi-agent system with RAG, chat, quiz, research, summarization, and search capabilities.

🚀 Features
🔹 Backend (Fully Working)

Chat agent

Quiz agent

RAG agent

Search agent

Summarization agent

Vector store database

Multiple Python modules

Fast execution

🔹 Frontend (Work in Progress)

Streamlit-based UI

Simple interface for interacting with AI agents

More pages coming soon

🛠️ Tech Stack

Backend:

Python

LangChain / agents

Vector Store

Custom agent scripts

Frontend:

Streamlit

📁 Project Structure
AI_RESEARCH_COMPANION/
│── backend/
│── streamlit_app/
│── vector_store/
│── requirements.txt
│── .env
│── .gitignore

⚙️ Setup Instructions
1️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate  (Linux/Mac)
venv\Scripts\activate     (Windows)

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Add your Environment Variables

Create .env:

API_KEY=your_key
MODEL=your_model

4️⃣ Run the backend
python backend/main.py

5️⃣ Run the Streamlit frontend
streamlit run streamlit_app/main.py

🚧 Roadmap

Add beautiful frontend UI

Integrate all agents

Add user authentication

Add file upload features

Improve vector database