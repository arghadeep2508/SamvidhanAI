import json
import re

# load constitution data
with open("database/constitution.json", "r", encoding="utf-8") as f:
    constitution_data = json.load(f)


def search_articles(query):

    query = query.lower()

    # extract number from query
    match = re.search(r"\d+", query)

    if match:
        article_number = int(match.group())

        results = []

        for art in constitution_data:

            try:
                # convert article field to int safely
                art_number = int(str(art["article"]).replace("A",""))

                if art_number == article_number:
                    results.append(art)

            except:
                continue

        return results

    # fallback keyword search
    results = []

    for art in constitution_data:

        if query in art["title"].lower() or query in art["description"].lower():
            results.append(art)

    return results