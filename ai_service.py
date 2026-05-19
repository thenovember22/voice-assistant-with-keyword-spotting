import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

SYSTEM_PROMPT = (
    "You are Maya, a sharp and helpful AI assistant. "
    "Answer clearly and concisely in 2 to 3 sentences unless the user asks for more."
)


def ask_ai(prompt: str) -> str:
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Groq is not configured yet. Please add your GROQ_API_KEY."

    try:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            model="llama-3.3-70b-versatile",
        )
        reply = chat_completion.choices[0].message.content
        return reply.strip() if reply else "I could not find an answer for that."
    except Exception as exc:
        print("Groq Error:", exc)
        return "I could not reach Groq right now."


ask_gemini = ask_ai
