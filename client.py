from groq import Groq


client = Groq(api_key="YOUR_GROQ_API_KEY")

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain recursion",
        }
    ],
    model="llama-3.3-70b-versatile",
)

print(chat_completion.choices[0].message.content)
