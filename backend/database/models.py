from .db_connection import get_db

def save_report(topic, summary, quiz):
    db = get_db()
    reports = db["reports"]
    report_data = {
        "topic": topic,
        "summary": summary,
        "quiz": quiz
    }
    reports.insert_one(report_data)
    print(f"✅ Report for '{topic}' saved successfully in MongoDB!")
