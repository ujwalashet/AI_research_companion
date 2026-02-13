import io
from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
import pytesseract
import fitz  # PyMuPDF

from transformers import pipeline

from backend.agents.summarize_agent import summarize_text
from backend.agents.quiz_agent import generate_quiz
from backend.agents.rag_agent import store_document_in_vector_db, query_vector_db

# Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()

# ---------------------------
# Load local QA model (once)
# ---------------------------
qa_model = pipeline(
    "question-answering",
    model="deepset/bert-base-cased-squad2"
)

@app.get("/")
def home():
    return {"message": "AI Research Companion (Offline Version) running 🚀"}

# ---------------------------
# Upload PDF + Summarize
# ---------------------------
@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    extracted_text = ""
    for page in pdf_doc:
        extracted_text += page.get_text()

    summary = summarize_text("PDF Content", extracted_text)

    # Quiz disabled for stability
    quiz = []

    return {
        "filename": file.filename,
        "summary": summary,
        "quiz": quiz
    }

# ---------------------------
# Upload Image (OCR)
# ---------------------------
@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    extracted_text = pytesseract.image_to_string(image)
    summary = summarize_text("Image Content", extracted_text)

    return {
        "filename": file.filename,
        "summary": summary
    }

# ---------------------------
# Upload document to RAG
# ---------------------------
@app.post("/upload_to_rag")
async def upload_to_rag(file: UploadFile = File(...)):
    ext = file.filename.lower().split(".")[-1]
    data = await file.read()
    content = ""

    if ext == "pdf":
        pdf = fitz.open(stream=data, filetype="pdf")
        for page in pdf:
            content += page.get_text()
    elif ext in ["jpg", "jpeg", "png"]:
        image = Image.open(io.BytesIO(data))
        content = pytesseract.image_to_string(image)
    else:
        content = data.decode()

    store_document_in_vector_db(content, file.filename)

    return {"message": "Document stored for RAG"}

# ---------------------------
# RAG Chat (Local QA)
# ---------------------------
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
        "confidence": result["score"]
    }
