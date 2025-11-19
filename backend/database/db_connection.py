from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    mongo_url = os.getenv("MONGO_URL")
    client = MongoClient(mongo_url)
    db = client["ai_research_db"]
    return db
