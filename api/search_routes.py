from flask import Blueprint, request, jsonify
from services.legal_advisor import legal_answer

search_bp = Blueprint("search", __name__)

@search_bp.route("/api/ask", methods=["GET"])
def ask():

    question = request.args.get("q")

    if not question:
        return jsonify({"answer": "Please enter a question."})

    answer = legal_answer(question)

    return jsonify({"answer": answer})