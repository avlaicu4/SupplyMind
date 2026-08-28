import os

from dotenv import load_dotenv
from openai import (
    APIConnectionError,
    AuthenticationError,
    NotFoundError,
    OpenAI,
    OpenAIError,
    RateLimitError,
)

from .inventory_services import generate_reorder_recommendations

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")


SYSTEM_PROMPT = (
    "You are ProcureAI, an AI procurement assistant for a small business. "
    "Use only the inventory recommendations provided by the backend. "
    "Do not invent products, suppliers, prices, or delivery times. "
    "If information is missing, say what is missing. "
    "Answer clearly, practically, and briefly."
)


def ask_inventory_agent(user_message: str, db):
    if not os.getenv("OPENAI_API_KEY"):
        return (
            "OpenAI API key is not configured. "
            "Set OPENAI_API_KEY in the backend environment to enable the hosted AI assistant."
        )

    recommendations = generate_reorder_recommendations(db)
    client = OpenAI()

    try:
        response = client.responses.create(
            model=OPENAI_MODEL,
            instructions=SYSTEM_PROMPT,
            input=[
                {
                    "role": "user",
                    "content": (
                        f"User question: {user_message}\n\n"
                        f"Inventory recommendations from backend: {recommendations}"
                    ),
                },
            ],
        )

        return response.output_text
    except AuthenticationError:
        return "OpenAI authentication failed. Check if OPENAI_API_KEY is correct."
    except NotFoundError:
        return (
            f"OpenAI model '{OPENAI_MODEL}' was not found or is not available "
            "for your account. Try setting OPENAI_MODEL to another model."
        )
    except RateLimitError:
        return (
            "OpenAI rate limit or quota was reached. Check your OpenAI billing "
            "and usage limits."
        )
    except APIConnectionError:
        return "Could not connect to OpenAI. Check your internet connection."
    except OpenAIError as error:
        return f"OpenAI API error: {error}"
