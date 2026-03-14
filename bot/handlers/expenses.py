from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from bot.db.database import add_expense, delete_expense
from bot.keyboards.inline import categories_keyboard, skip_keyboard
from bot.utils.formatters import fmt_expense_saved

router = Router()


class ExpenseForm(StatesGroup):
    amount = State()
    category = State()
    description = State()


# --- /add command ---

@router.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext) -> None:
    await state.set_state(ExpenseForm.amount)
    await message.answer("Введи сумму:")


# --- Quick add: plain number message ---

@router.message(F.text.regexp(r"^\d+([.,]\d+)?$"))
async def quick_add_amount(message: Message, state: FSMContext) -> None:
    amount = float(message.text.replace(",", "."))
    await state.update_data(amount=amount)
    await state.set_state(ExpenseForm.category)
    await message.answer(
        f"Сумма: <b>{amount:,.0f} ₽</b>\nВыбери категорию:",
        reply_markup=categories_keyboard(),
        parse_mode="HTML",
    )


# --- FSM: waiting for amount ---

@router.message(ExpenseForm.amount)
async def fsm_amount(message: Message, state: FSMContext) -> None:
    try:
        amount = float(message.text.replace(",", ".").replace(" ", ""))
        if amount <= 0:
            raise ValueError
    except (ValueError, AttributeError):
        await message.answer("Введи корректное положительное число:")
        return

    await state.update_data(amount=amount)
    await state.set_state(ExpenseForm.category)
    await message.answer(
        f"Сумма: <b>{amount:,.0f} ₽</b>\nВыбери категорию:",
        reply_markup=categories_keyboard(),
        parse_mode="HTML",
    )


# --- FSM: category selected ---

@router.callback_query(ExpenseForm.category, F.data.startswith("cat:"))
async def fsm_category(callback: CallbackQuery, state: FSMContext) -> None:
    category = callback.data.split(":")[1]
    await state.update_data(category=category)
    await state.set_state(ExpenseForm.description)
    await callback.message.edit_text(
        "Добавь описание? (необязательно)",
        reply_markup=skip_keyboard(),
    )
    await callback.answer()


# --- FSM: description ---

@router.message(ExpenseForm.description)
async def fsm_description(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    expense_id = await add_expense(
        user_id=message.from_user.id,
        amount=data["amount"],
        category=data["category"],
        description=message.text.strip(),
    )
    await message.answer(
        fmt_expense_saved(data["amount"], data["category"], message.text.strip()),
        parse_mode="HTML",
    )


@router.callback_query(ExpenseForm.description, F.data == "skip_description")
async def fsm_skip_description(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    await add_expense(
        user_id=callback.from_user.id,
        amount=data["amount"],
        category=data["category"],
        description=None,
    )
    await callback.message.edit_text(
        fmt_expense_saved(data["amount"], data["category"], None),
        parse_mode="HTML",
    )
    await callback.answer()


# --- Delete via /delN command ---

@router.message(F.text.regexp(r"^/del\d+$"))
async def cmd_delete(message: Message) -> None:
    expense_id = int(message.text[4:])
    deleted = await delete_expense(expense_id, message.from_user.id)
    if deleted:
        await message.answer(f"🗑 Трата #{expense_id} удалена.")
    else:
        await message.answer("Трата не найдена или не принадлежит тебе.")
