from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.db.database import get_monthly_expenses, get_recent_expenses
from bot.utils.formatters import fmt_report, fmt_history

router = Router()


@router.message(Command("report"))
async def cmd_report(message: Message) -> None:
    now = datetime.now()
    expenses = await get_monthly_expenses(message.from_user.id, now.year, now.month)
    await message.answer(fmt_report(expenses, now.year, now.month), parse_mode="HTML")


@router.message(Command("history"))
async def cmd_history(message: Message) -> None:
    expenses = await get_recent_expenses(message.from_user.id, limit=10)
    await message.answer(fmt_history(expenses), parse_mode="HTML")
