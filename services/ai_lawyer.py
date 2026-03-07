from groq import Groq

client = Groq(api_key="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")

def explain_law(question, article_text):

    prompt = f"""
You are SamvidhanAI, an assistant explaining the Constitution of India.

Respond in clear professional English.

User Question:
{question}

Relevant Article:
{article_text}

Explain:
- What the article means
- Why it is important
- What rights citizens have
- Simple real-life example
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content