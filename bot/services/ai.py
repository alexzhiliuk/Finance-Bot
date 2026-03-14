import json
from io import BytesIO

from openai import AsyncOpenAI

from bot.config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

PARSE_SYSTEM_PROMPT = """You are a finance assistant. Extract expense data from user text (any language).

Return a JSON object with exactly these fields:
- "amount": a positive number (required)
- "category": one of: food, transport, shopping, entertainment, health, other
- "description": short description string, or null

If you cannot find a clear amount, return: {"error": "no_amount"}

Examples:
  "spent 500 on lunch at cafe" → {"amount": 500, "category": "food", "description": "lunch at cafe"}
  "metro ticket 60 rubles" → {"amount": 60, "category": "transport", "description": "metro ticket"}
  "bought shoes 3500" → {"amount": 3500, "category": "shopping", "description": "shoes"}
  "just talking" → {"error": "no_amount"}
"""


async def transcribe_voice(voice_bytes: bytes, filename: str = "voice.ogg") -> str:
    """Transcribe a voice message using Whisper."""
    audio_file = (filename, BytesIO(voice_bytes), "audio/ogg")
    transcript = await client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
    )
    return transcript.text


async def parse_expense_text(text: str) -> dict:
    """Use GPT-4o-mini to extract expense data from natural language."""
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": PARSE_SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return json.loads(response.choices[0].message.content)
