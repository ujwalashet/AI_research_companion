from tavily import TavilyClient
import os

def search_topic(topic):
    """
    Uses Tavily Web Search API for real-time research.
    """

    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    response = client.search(
        query=topic,
        max_results=5
    )

    # Extract the content of all search hits
    if "results" in response:
        results_text = "\n\n".join([r["content"] for r in response["results"]])
    else:
        results_text = f"No results found for {topic}."

    return results_text
