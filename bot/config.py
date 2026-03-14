import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.environ["BOT_TOKEN"]
OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]

# Comma-separated Telegram user IDs allowed to use the bot, e.g. "123456789,987654321"
_raw_ids = os.getenv("ALLOWED_USER_IDS", "")
ALLOWED_USER_IDS: set[int] = {int(i.strip()) for i in _raw_ids.split(",") if i.strip()}

CATEGORIES: dict[str, str] = {
    "food": "🍕 Еда",
    "transport": "🚗 Транспорт",
    "shopping": "🛍 Покупки",
    "entertainment": "🎬 Развлечения",
    "health": "💊 Здоровье",
    "other": "📦 Другое",
}
