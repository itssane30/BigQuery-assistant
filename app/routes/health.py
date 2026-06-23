"""
app/routes/health.py
------------------------
    GET /health
    Returns: {"vertex": "connected", "bigquery": "connected", "mcp": "connected"}
"""

import asyncio
from flask import Blueprint, jsonify

from app.mcp.client import BigQueryMCPClient
from app.services.bigquery import check_bigquery_connection
from app.services.vertex import get_genai_client
from app.utils.logger import get_logger

logger = get_logger(__name__)

health_bp = Blueprint("health", __name__)


async def _check_mcp() -> bool:
    try:
        async with BigQueryMCPClient() as client:
            await client.list_tools()
        return True
    except Exception as exc:
        logger.warning(f"MCP health check failed: {exc}")
        return False


def _check_vertex() -> bool:
    try:
        get_genai_client()
        return True
    except Exception as exc:
        logger.warning(f"Vertex AI health check failed: {exc}")
        return False


@health_bp.route("/health", methods=["GET"])
def health():
    vertex_ok = _check_vertex()
    bigquery_ok = check_bigquery_connection()
    mcp_ok = asyncio.run(_check_mcp())

    status = {
        "vertex": "connected" if vertex_ok else "error",
        "bigquery": "connected" if bigquery_ok else "error",
        "mcp": "connected" if mcp_ok else "error",
    }
    overall_ok = vertex_ok and bigquery_ok and mcp_ok
    return jsonify(status), (200 if overall_ok else 503)
