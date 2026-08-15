from ollama import chat

from .inventory_services import generate_reorder_recommendations

OLLAMA_MODEL = "llama3.1:8b"


def ask_inventory_agent(user_message: str, db):
    recommendations = generate_reorder_recommendations(db)

    response = chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are ProcureAI, an AI procurement assistant for a small business. "
                    "Use only the inventory recommendations provided by the backend. "
                    "Do not invent products, suppliers, prices, or delivery times. "
                    "Answer clearly and briefly."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"User question: {user_message}\n\n"
                    f"Inventory recommendations: {recommendations}"
                ),
            },
        ],
    )

    return response["message"]["content"]