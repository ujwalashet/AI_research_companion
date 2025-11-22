from langchain_openai import ChatOpenAI
import json

def generate_quiz(summary_text):
    """
    Generate quiz in list format:
    [
        {
            "question": "...",
            "options": ["A","B","C","D"],
            "answer": "B"
        },
        ...
    ]
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)

    prompt = f"""
    Create exactly 3 multiple-choice questions from this summary:

    {summary_text}

    Return the result STRICTLY in this JSON format only:

    [
      {{
        "question": "text?",
        "options": ["A","B","C","D"],
        "answer": "correct option value"
      }}
    ]

    Do NOT include explanations. Do NOT include text outside JSON.
    """

    response = llm.invoke(prompt).content

    # Try converting the output to proper JSON
    try:
        quiz = json.loads(response)
        return quiz
    except:
        return []
