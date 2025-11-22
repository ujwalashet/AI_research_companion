import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import pytesseract
from PIL import Image
import io
from backend.database.db_connection import get_db
from backend.agents.chat_agent import generate_chat_reply
from bson import ObjectId
import base64
from fastapi import UploadFile, File
from openai import OpenAI

from langchain_openai import ChatOpenAI

from fastapi import UploadFile, File
import fitz  # PyMuPDF
from fastapi import FastAPI, Form
from dotenv import load_dotenv
import os

from backend.database.models import save_report
from backend.agents.search_agent import search_topic
from backend.agents.summarize_agent import summarize_text
from backend.agents.quiz_agent import generate_quiz

from fastapi import UploadFile, File, Form
from openai import OpenAI
import base64
import fitz
from backend.agents.rag_agent import store_document_in_vector_db, query_vector_db


from transformers import pipeline

# Load HuggingFace QA model only once
qa_model = pipeline(
    "question-answering",
    model="deepset/bert-base-cased-squad2"
)

client = OpenAI()

load_dotenv()

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Research Companion (LangChain Version) is running 🚀"}

@app.post("/research")
def research_topic(topic: str = Form(...)):
    """
    Multi-step agent flow: Search -> Summarize -> Quiz -> Save
    """

    # Step 1: Search
    search_results = search_topic(topic)

    # Step 2: Summarize
    summary = summarize_text(topic, search_results)

    # Step 3: Quiz generation
    quiz = generate_quiz(summary)

    # Step 4: Save to MongoDB
    save_report(topic, summary, quiz)

    return {
        "topic": topic,
        "summary": summary,
        "quiz": quiz
    }
@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    extracted_text = ""

    for page in pdf_doc:
        extracted_text += page.get_text()

    summary = summarize_text("PDF Content", extracted_text)
    quiz = generate_quiz(summary)

    save_report(file.filename, summary, quiz)

    return {
        "filename": file.filename,
        "extracted_content": extracted_text,
        "summary": summary,
        "quiz": quiz
    }


@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    """
    Extract text from image using Tesseract OCR + generate summary + quiz.
    """

    # Step 1: Read image
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # Step 2: Extract text with Tesseract OCR
    try:
        extracted_text = pytesseract.image_to_string(image)
    except Exception as e:
        return {"error": f"OCR failed: {str(e)}"}

    # Step 3: Summarize the extracted text
    summary = summarize_text("Image OCR Content", extracted_text)

    # Step 4: Generate quiz
    quiz = generate_quiz(summary)

    # Step 5: Save to mongoDB
    save_report(file.filename, summary, quiz)

    return {
        "filename": file.filename,
        "extracted_text": extracted_text,
        "summary": summary,
        "quiz": quiz
    }

@app.post("/upload_text")
async def upload_text(text: str = Form(...)):
    """
    Accepts raw text, summarizes it, generates quiz, and saves to DB.
    """
    # Step 1: Summarize
    summary = summarize_text("User Text Input", text)

    # Step 2: Quiz
    quiz = generate_quiz(summary)

    # Step 3: Save to DB
    save_report("Text Input", summary, quiz)

    return {
        "input_text": text,
        "summary": summary,
        "quiz": quiz
    }
@app.post("/chat_with_report")
def chat_with_report(report_id: str, question: str):
    """
    User asks a question about a saved report (PDF/Image/Text/Research).
    """
    db = get_db()
    reports = db["reports"]

    # Find the report in MongoDB
    report = reports.find_one({"_id": ObjectId(report_id)})

    if not report:
        return {"error": "Report not found"}

    summary = report["summary"]  # Use the saved summary
    answer = generate_chat_reply(summary, question)

    return {
        "report_id": report_id,
        "question": question,
        "answer": answer
    }

@app.post("/generate_mindmap")
async def generate_mindmap(text: str = Form(...)):
    """
    Converts any text into a hierarchical mindmap using GPT.
    """

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)

    prompt = f"""
    Convert the following text into a clear, structured mindmap.
    Use this format:
    - Main Topic
        - Subtopic 1
            - Point
            - Point
        - Subtopic 2
            - Point

    Text:
    {text}
    """

    response = llm.invoke(prompt)

    return {
        "mindmap": response.content
    }
# ----------------------------
# RAG Upload API
# ----------------------------
# ----------------------------
# RAG Upload API
# ----------------------------
@app.post("/upload_to_rag")
async def upload_to_rag(file: UploadFile = File(...)):
    ext = file.filename.lower().split(".")[-1]
    content = ""
    data = await file.read()

    # 1. Extract text from PDF
    if ext == "pdf":
        pdf = fitz.open(stream=data, filetype="pdf")
        for page in pdf:
            content += page.get_text()

    # 2. Extract text from image using FREE offline OCR
    elif ext in ["jpg", "jpeg", "png"]:
        image = Image.open(io.BytesIO(data))
        content = pytesseract.image_to_string(image)

    # 3. Plain Text File
    else:
        content = data.decode()

    # Store extracted text in Vector DB
    store_document_in_vector_db(content, file.filename)

    return {
        "message": "Document stored in Vector DB (RAG Ready)!",
        "filename": file.filename
    }
# ----------------------------
# RAG Chat API
# ----------------------------
@app.get("/rag_chat")
def rag_chat(question: str):
    context = query_vector_db(question)

    if not context:
        return {"answer": "No relevant document found."}

    result = qa_model({
        "question": question,
        "context": context
    })

    return {
        "question": question,
        "answer": result["answer"],
        "score": result["score"],
        "context_used": context
    }
@app.post("/upload_text_to_rag")
async def upload_text_to_rag(text: str = Form(...)):
    store_document_in_vector_db(text, "text_input")
    return {"message": "Text stored in vector DB!"}

@app.get("/debug_quiz")
def debug_quiz():
    summary = "This is a test summary about AI."
    quiz = generate_quiz(summary)
    return {"quiz": quiz}
