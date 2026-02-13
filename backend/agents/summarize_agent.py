from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def summarize_text(topic, context_text):
    if not context_text or len(context_text.strip()) == 0:
        return "No content found to summarize."

    context_text = context_text[:3000]

    summary = summarizer(
        context_text,
        max_length=150,
        min_length=60,
        do_sample=False
    )

    return summary[0]["summary_text"]
