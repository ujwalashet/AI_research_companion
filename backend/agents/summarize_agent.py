from langchain_openai import ChatOpenAI

def summarize_text(topic, context_text):
    """
    Uses LangChain + OpenAI to summarize text into a detailed explanation.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    prompt = f"Summarize the following information about {topic} in around 10 lines:\n\n{context_text}"
    response = llm.invoke(prompt)
    return response.content
