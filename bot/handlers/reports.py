from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.db.database import get_daily_expenses, get_monthly_expenses, get_recent_expenses
from bot.keyboards.inline import days_keyboard, months_keyboard
from bot.utils.formatters import fmt_day_report, fmt_detail_report, fmt_history, fmt_report

router = Router()


@router.message(Command("report"))
async def cmd_report(message: Message) -> None:
    await message.answer("Выберите месяц:", reply_markup=months_keyboard("month"))


@router.callback_query(F.data.startswith("month:"))
async def on_month_selected(callback: CallbackQuery) -> None:
    _, year, month = callback.data.split(":")
    year, month = int(year), int(month)
    expenses = await get_monthly_expenses(callback.from_user.id, year, month)
    await callback.message.edit_text(fmt_report(expenses, year, month), parse_mode="HTML")
    await callback.answer()


@router.message(Command("day"))
async def cmd_day(message: Message) -> None:
    await message.answer("Выберите месяц:", reply_markup=months_keyboard("daym"))


@router.callback_query(F.data.startswith("daym:"))
async def on_day_month_selected(callback: CallbackQuery) -> None:
    _, year, month = callback.data.split(":")
    year, month = int(year), int(month)
    await callback.message.edit_text(
        "Выберите день:", reply_markup=days_keyboard(year, month)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("day:"))
async def on_day_selected(callback: CallbackQuery) -> None:
    _, year, month, day = callback.data.split(":")
    year, month, day = int(year), int(month), int(day)
    expenses = await get_daily_expenses(callback.from_user.id, year, month, day)
    await callback.message.edit_text(
        fmt_day_report(expenses, year, month, day), parse_mode="HTML"
    )
    await callback.answer()


@router.message(Command("detail"))
async def cmd_detail(message: Message) -> None:
    await message.answer("Выберите месяц:", reply_markup=months_keyboard("detm"))


@router.callback_query(F.data.startswith("detm:"))
async def on_detail_month_selected(callback: CallbackQuery) -> None:
    _, year, month = callback.data.split(":")
    year, month = int(year), int(month)
    expenses = await get_monthly_expenses(callback.from_user.id, year, month)
    await callback.message.edit_text(
        fmt_detail_report(expenses, year, month), parse_mode="HTML"
    )
    await callback.answer()


@router.message(Command("history"))
async def cmd_history(message: Message) -> None:
    expenses = await get_recent_expenses(message.from_user.id, limit=10)
    await message.answer(fmt_history(expenses), parse_mode="HTML")
