import json
import re

# Load constitution database
with open("database/constitution.json", "r", encoding="utf-8") as f:
    constitution_data = json.load(f)

# Keyword → Article mapping
keyword_map = {

    # Article 21
    "life": 21,
    "liberty": 21,
    "privacy": 21,
    "personal liberty": 21,

    # Article 19
    "speech": 19,
    "expression": 19,
    "freedom": 19,
    "media": 19,
    "press": 19,

    # Article 14
    "equality": 14,
    "equal": 14,
    "discrimination": 14,

    # Article 22
    "arrest": 22,
    "police": 22,
    "detention": 22,
    "custody": 22,
    "warrant": 22,
    "lawyer": 22,

    # search / seizure cases
    "phone": 21,
    "search": 21,
    "seizure": 21

}

def search_articles(question):

    question = question.lower()

    # -------- Article number detection --------
    match = re.search(r"\d+", question)

    if match:
        article_number = int(match.group())

        for item in constitution_data:

            if not isinstance(item, dict):
                continue

            if item.get("article") == article_number:
                return format_response(item)

    # -------- Keyword detection --------
    for keyword, article_number in keyword_map.items():

        if keyword in question:

            for item in constitution_data:

                if not isinstance(item, dict):
                    continue

                if item.get("article") == article_number:
                    return format_response(item)

    return "I could not find a relevant article in the Constitution database."


def format_response(article):

    title = article.get("title", "")
    description = article.get("description", "")

    response = f"""
Relevant Articles:
Article {article.get("article")}

Explanation:
{description}

Citizen Advice:
For detailed legal understanding, consult a qualified lawyer or refer to the official constitutional text.
"""

    return response.strip()