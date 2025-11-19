from langchain_openai import ChatOpenAI

def generate_quiz(summary_text):
    """
    Uses LangChain to create quiz questions and answers based on the summary.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    prompt = f"Create 3 multiple-choice quiz questions with answers from the following summary:\n\n{summary_text}"
    response = llm.invoke(prompt)
    return response.content
