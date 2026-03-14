from aiogram import Router, F, Bot
from aiogram.types import Message

from bot.db.database import add_expense
from bot.services.ai import transcribe_voice, parse_expense_text
from bot.utils.formatters import fmt_expense_saved

router = Router()


@router.message(F.voice)
async def voice_handler(message: Message, bot: Bot) -> None:
    status = await message.answer("🎙 Обрабатываю голосовое...")

    try:
        # Скачиваем голосовое
        voice_io = await bot.download(message.voice)
        voice_bytes = voice_io.read()

        # Транскрибируем через Whisper
        text = await transcribe_voice(voice_bytes)
        await status.edit_text(f"🎙 Распознано: <i>{text}</i>\n⏳ Разбираю...", parse_mode="HTML")

        # Парсим через GPT
        parsed = await parse_expense_text(text)

        if "error" in parsed:
            await status.edit_text(
                f"🎙 Распознано: <i>{text}</i>\n\n"
                "❌ Не удалось найти сумму. Попробуй сказать, например: <i>«потратил 500 на кофе»</i>.",
                parse_mode="HTML",
            )
            return

        amount = float(parsed["amount"])
        category = parsed.get("category", "other")
        description = parsed.get("description") or None

        await add_expense(
            user_id=message.from_user.id,
            amount=amount,
            category=category,
            description=description,
        )

        await status.edit_text(
            f"🎙 Распознано: <i>{text}</i>\n\n" + fmt_expense_saved(amount, category, description),
            parse_mode="HTML",
        )

    except Exception as e:
        await status.edit_text(f"❌ Ошибка при обработке голосового: {e}")
