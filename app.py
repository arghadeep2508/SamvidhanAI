from flask import Flask, render_template, request, jsonify
from groq import Groq
from search_engine import search_articles
import os
app = Flask(__name__)

# -----------------------------
# GROQ API CONFIG
# -----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


# -----------------------------
# HOMEPAGE
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/how-to-use")
def how_to_use():
    return render_template("how-to-use.html")

# -----------------------------
# CHAT API
# -----------------------------
@app.route("/api/ask")
def ask():

    try:

        question = request.args.get("q")

        if not question:
            return jsonify({"answer": "Please enter a question."})

        question_lower = question.lower().strip()

        # -----------------------------
        # GREETING HANDLER
        # -----------------------------
        greetings = ["hi", "hello", "hey", "hi buddy", "hello buddy"]

        if question_lower in greetings:
            return jsonify({
                "answer": "Hello. I am SamvidhanAI — your assistant for understanding the Constitution of India. You can ask me about constitutional articles, citizen rights, or legal situations."
            })

        # -----------------------------
        # THANK YOU HANDLER
        # -----------------------------
        thanks = ["thanks", "thank you", "thanks buddy", "thank you buddy"]

        if question_lower in thanks:
            return jsonify({
                "answer": "You're welcome. If you have more questions about the Constitution of India, feel free to ask."
            })

        # -----------------------------
        # SEARCH CONSTITUTION DATABASE
        # -----------------------------
        articles = search_articles(question)

        context = ""

        # Case 1: articles returned as list
        if isinstance(articles, list):

            for art in articles:

                if not isinstance(art, dict):
                    continue

                article_no = art.get("article", "")
                title = art.get("title", "")
                description = art.get("description", "")

                context += f"""
Article {article_no} — {title}

{description}

"""

        # Case 2: search returned a text string
        elif isinstance(articles, str):

            context = articles

        # Case 3: nothing found
        if not context:
            context = "No specific article found in the Constitution database."

        # -----------------------------
        # SYSTEM PROMPT
        # -----------------------------
        system_prompt = f"""
You are SamvidhanAI, an assistant that explains the Constitution of India.

Use ONLY the constitutional context provided below when possible.

Context:
{context}

Rules:

- Do NOT start with greetings.
- Explain clearly in simple English.
- Mention relevant Article numbers when available.
- If the constitution does NOT directly mention something, clearly say so.
- Do NOT invent laws or sections.

Format answers like:

Relevant Articles:
(list them)

Explanation:
(simple explanation)

Citizen Advice:
(practical guidance)
"""

        # -----------------------------
        # AI REQUEST
        # -----------------------------
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.2,
            max_tokens=600
        )

        answer = completion.choices[0].message.content

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Server Error: {str(e)}"})


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)