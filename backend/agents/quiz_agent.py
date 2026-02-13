def generate_quiz(summary_text: str):
    if not summary_text:
        return []

    sentences = summary_text.split(".")
    questions = []

    for sentence in sentences[:5]:
        sentence = sentence.strip()
        if len(sentence) > 20:
            questions.append({
                "question": f"What does this mean?\n{sentence}",
                "answer": sentence
            })

    return questions
