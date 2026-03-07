from services.search_service import search_articles
from services.ai_lawyer import explain_law

def legal_answer(question):

    greetings = ["hi", "hello", "hey"]

    if question.lower().strip() in greetings:
        return "Hello! I am SamvidhanAI. Ask me anything about the Constitution of India."

    articles = search_articles(question)

    if not articles:
        return "I could not find a specific constitutional article. Try asking about rights, police powers, arrest, freedom, or property."

    article = articles[0]

    explanation = explain_law(question, article["content"])

    return f"""
### Relevant Constitutional Provision

**{article['title']}**

{explanation}
"""