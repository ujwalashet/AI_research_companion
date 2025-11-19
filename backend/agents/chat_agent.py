from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def build_system_prompt(summary):
    prompt = "You are a helpful research assistant. "
    prompt += "Answer the user's questions using this summary: \n\n"
    prompt += summary
    prompt += "\n\nGive short and clear answers. If user asks something not in summary, then clearly say you don’t know."
    return prompt

def generate_chat_reply(summary, user_question):
    """
    Generates a chat reply using OpenAI, grounded on the summary.
    """
    system_prompt = build_system_prompt(summary)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ]
    )

    return response.choices[0].message.content
