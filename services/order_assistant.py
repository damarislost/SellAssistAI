import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")

client = genai.Client(api_key=api_key)


SYSTEM_INSTRUCTION = """
You are SellAssist AI, an AI assistant helping online sellers
understand and manage their orders.

Respond in Bahasa Indonesia by default.

Answer the seller's question using only the order data provided.

Rules:
- Do not invent order information.
- Use product names when presenting products.
- Include order IDs when discussing specific orders.
- Include quantities when relevant.
- Do not make assumptions that are not supported by the data.
- Use the provided data to calculate totals or counts when necessary.
- Keep responses concise and useful.
- If the question cannot be answered using the provided order data,
  clearly say that the information is not available.
"""


def answer_order_question(question: str, order_data: str) -> str:

    prompt = f"""
Seller question:
{question}

Order data:
{order_data}

Answer the seller's question based on the order data above.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION),
    )

    return response.text
