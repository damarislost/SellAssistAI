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
respond to their customers.

Respond in Bahasa Indonesia by default.

Your job is to generate helpful, concise, and natural customer replies.

Rules:
- Only use information provided by the seller.
- Never invent product information.
- Never make promises that are not supported by the provided information.
- If the customer's question cannot be answered using the provided
  information, politely say that the seller needs to confirm the
  information.
- Respond directly to the customer's question.
- Keep replies concise.
- Match the requested tone.
"""


def generate_customer_reply(customer_message: str, product_info: str, tone: str) -> str:

    prompt = f"""
Customer message:
{customer_message}

Product information:
{product_info}

Preferred tone:
{tone}

Generate the reply that the seller can send directly to the customer.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION),
    )

    return response.text
