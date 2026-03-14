from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

HELP_TEXT = """
👋 <b>Финансовый бот</b>

Записывай расходы текстом или <b>голосовым сообщением</b>!

<b>Команды:</b>
/add — добавить трату пошагово
/report — отчёт за текущий месяц
/history — последние 10 трат
/help — показать это сообщение

<b>Быстрое добавление:</b>
Просто отправь число: <code>500</code> — и выбери категорию.

<b>Голос:</b>
Отправь голосовое, например <i>«потратил 250 на кофе»</i> — я всё запишу сам.
"""


@router.message(Command("start", "help"))
async def cmd_start(message: Message) -> None:
    await message.answer(HELP_TEXT, parse_mode="HTML")
