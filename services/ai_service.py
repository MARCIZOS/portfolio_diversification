"""AI explanation service powered by Groq with lightweight RAG."""

import json
import logging
import os

from groq import Groq

from services.query_service import build_query
# from services.rag_service import retrieve_context

def retrieve_context(query: str, top_k: int = 3) -> str:
    return "Mock RAG context due to missing dependencies."

DEFAULT_GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
REQUEST_TIMEOUT_SECONDS = 20
logger = logging.getLogger(__name__)


def _build_prompt(data: dict, context: str) -> str:
    """Build a concise structured prompt for risk explanation."""
    context_block = context.strip() if context else "No additional context retrieved."
    return (
        "You are a financial risk analyst.\n"
        "Explain the portfolio risk in simple terms for a non-technical investor.\n"
        "Include: diversification quality, risk concentration, stress vulnerability, and downside risk.\n"
        "Avoid technical jargon and keep the explanation practical and concise (120-180 words).\n\n"
        f"Retrieved context:\n{context_block}\n\n"
        f"Portfolio analysis data:\n{json.dumps(data, indent=2)}"
    )


def generate_portfolio_explanation(data: dict) -> dict[str, object]:
    """Generate human-readable explanation using Groq chat completion API."""
    api_key = os.getenv("GROQ_API_KEY")
    debug_enabled = bool(data.get("debug_rag")) or os.getenv("RAG_DEBUG", "").lower() in {
        "1",
        "true",
        "yes",
    }
    sanitized_data = {key: value for key, value in data.items() if key != "debug_rag"}
    query = build_query(sanitized_data)
    context = retrieve_context(query)
    
    if not api_key:
        logger.warning("GROQ_API_KEY not found in environment variables")
        explanation = (
            "AI explanation unavailable: GROQ_API_KEY is not configured. "
            "Set the key in .env file to enable generated insights."
        )
        if debug_enabled:
            return {
                "explanation": explanation,
                "rag_debug": {
                    "query": query,
                    "retrieved_context": context,
                    "final_output": explanation,
                },
            }
        return {"explanation": explanation}

    try:
        logger.debug("Using Groq model: %s", DEFAULT_GROQ_MODEL)
        
        client = Groq(api_key=api_key, timeout=REQUEST_TIMEOUT_SECONDS)
        
        logger.debug("Groq client initialized; requesting completion")
        
        response = client.chat.completions.create(
            model=DEFAULT_GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You produce clear and accurate financial explanations."},
                {"role": "user", "content": _build_prompt(sanitized_data, context)},
            ],
            temperature=0.2,
        )
        
        logger.debug("Groq API response received")
        
        content = response.choices[0].message.content
        if not content:
            logger.warning("Empty response from Groq model")
            explanation = "AI explanation unavailable: empty response from Groq model."
            if debug_enabled:
                return {
                    "explanation": explanation,
                    "rag_debug": {
                        "query": query,
                        "retrieved_context": context,
                        "final_output": explanation,
                    },
                }
            return {"explanation": explanation}
        
        explanation = content.strip()
        logger.debug("AI explanation generated (length=%d)", len(explanation))
        if debug_enabled:
            return {
                "explanation": explanation,
                "rag_debug": {
                    "query": query,
                    "retrieved_context": context,
                    "final_output": explanation,
                },
            }
        return {"explanation": explanation}
        
    except TimeoutError as exc:
        error_msg = f"AI explanation unavailable: Groq API timeout ({REQUEST_TIMEOUT_SECONDS}s)"
        logger.error(error_msg)
        if debug_enabled:
            return {
                "explanation": error_msg,
                "rag_debug": {
                    "query": query,
                    "retrieved_context": context,
                    "final_output": error_msg,
                },
            }
        return {"explanation": error_msg}
    except Exception as exc:
        error_msg = f"AI explanation unavailable due to Groq API error: {str(exc)}"
        logger.exception("Groq API error")
        if debug_enabled:
            return {
                "explanation": error_msg,
                "rag_debug": {
                    "query": query,
                    "retrieved_context": context,
                    "final_output": error_msg,
                },
            }
        return {"explanation": error_msg}
