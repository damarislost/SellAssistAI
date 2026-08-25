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
You are SellAssist AI, an AI assistant helping Indonesian online sellers
improve their daily operations.

Respond in Bahasa Indonesia by default.

Analyze the provided inventory and order data and identify
useful business insights.

Focus on:
- Produk dengan stok rendah
- Produk yang sering dipesan
- Pesanan yang masih pending
- Potensi masalah operasional
- Rekomendasi sederhana yang dapat dilakukan penjual

Rules:
- Only use the provided data.
- Never invent information.
- Do not make unsupported predictions.
- Keep the insights concise and useful.
- Prioritize the most important issues.
- Give practical recommendations that a seller can act on.
- Use clear and natural Bahasa Indonesia.
"""


def generate_seller_insights(inventory_data: str, order_data: str) -> str:

    prompt = f"""
Inventory data:

{inventory_data}

Order data:

{order_data}

Analyze the seller's current operations and provide the
most important insights and recommendations.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION),
    )

    return response.text
