"""
app/routes/chat.py
---------------------
    POST /chat
    Input:  {"message": "Top customers by revenue"}
    Output: {"answer": "...", "sql": "...", "execution_time_sec": ..., "tool_calls": [...]}
"""

import asyncio
import time
from flask import Blueprint, jsonify, request

from app.agent.vertex_agent import answer_question
from app.utils.logger import get_logger

logger = get_logger(__name__)

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Field 'message' is required."}), 400

    logger.info(f"Incoming question: {message}")
    start = time.time()

    try:
        result = asyncio.run(answer_question(message))
    except Exception as exc:
        logger.exception("Agent failed to answer question")
        return jsonify({"error": str(exc)}), 500

    logger.info(f"Answered in {round(time.time() - start, 2)}s")

    return jsonify(
        {
            "answer": result["answer"],
            "sql": result["sql"],
            "execution_time_sec": result["execution_time_sec"],
            "tool_calls": result["tool_calls"],
        }
    )
