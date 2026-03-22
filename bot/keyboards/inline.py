import calendar
from datetime import datetime

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

from bot.config import CATEGORIES
from bot.utils.formatters import MONTHS_RU


def categories_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for key, label in CATEGORIES.items():
        builder.button(text=label, callback_data=f"cat:{key}")
    builder.adjust(2)
    return builder.as_markup()


def skip_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Пропустить", callback_data="skip_description")
    return builder.as_markup()


def months_keyboard(callback_prefix: str = "month") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    now = datetime.now()
    for i in range(12):
        month = now.month - i
        year = now.year
        if month <= 0:
            month += 12
            year -= 1
        label = f"{MONTHS_RU[month]} {year}"
        builder.button(text=label, callback_data=f"{callback_prefix}:{year}:{month}")
    builder.adjust(3)
    return builder.as_markup()


def days_keyboard(year: int, month: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    num_days = calendar.monthrange(year, month)[1]
    for day in range(1, num_days + 1):
        builder.button(text=str(day), callback_data=f"day:{year}:{month}:{day}")
    builder.adjust(7)
    return builder.as_markup()


def expense_actions_keyboard(expense_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🗑 Удалить", callback_data=f"del:{expense_id}")
    return builder.as_markup()
