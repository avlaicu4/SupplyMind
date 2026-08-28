import os

from anthropic import (
    APIConnectionError,
    APIError,
    Anthropic,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
)
from dotenv import load_dotenv

from .inventory_services import generate_reorder_recommendations

load_dotenv()

ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5")


SYSTEM_PROMPT = (
    "You are ProcureAI, an AI procurement assistant for a small business. "
    "Use only the inventory recommendations provided by the backend. "
    "Do not invent products, suppliers, prices, or delivery times. "
    "If information is missing, say what is missing. "
    "Answer clearly, practically, and briefly."
)


def ask_inventory_agent(user_message: str, db):
    if not os.getenv("ANTHROPIC_API_KEY"):
        return (
            "Claude API key is not configured. "
            "Set ANTHROPIC_API_KEY in the backend environment to enable the hosted AI assistant."
        )

    recommendations = generate_reorder_recommendations(db)
    client = Anthropic()

    try:
        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=600,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"User question: {user_message}\n\n"
                        f"Inventory recommendations from backend: {recommendations}"
                    ),
                },
            ],
        )

        text_blocks = [
            block.text
            for block in response.content
            if getattr(block, "type", None) == "text"
        ]

        return "\n".join(text_blocks).strip()
    except AuthenticationError:
        return "Claude authentication failed. Check if ANTHROPIC_API_KEY is correct."
    except NotFoundError:
        return (
            f"Claude model '{ANTHROPIC_MODEL}' was not found or is not available "
            "for your account. Try setting ANTHROPIC_MODEL to another model."
        )
    except RateLimitError:
        return (
            "Claude rate limit or quota was reached. Check your Anthropic billing "
            "and usage limits."
        )
    except APIConnectionError:
        return "Could not connect to Claude. Check your internet connection."
    except APIError as error:
        return f"Claude API error: {error}"
