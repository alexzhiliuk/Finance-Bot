from datetime import datetime

from bot.config import CATEGORIES

MONTHS_RU = {
    1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель",
    5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
    9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь",
}


def fmt_amount(amount: float) -> str:
    return f"{amount:,.0f}".replace(",", " ") + " Br"


def fmt_expense_saved(amount: float, category: str, description: str | None) -> str:
    label = CATEGORIES.get(category, category)
    desc = f" • {description}" if description else ""
    return f"✅ Записано: <b>{fmt_amount(amount)}</b> • {label}{desc}"


def fmt_report(expenses: list[dict], year: int, month: int) -> str:
    month_name = f"{MONTHS_RU[month]} {year}"

    if not expenses:
        return f"📊 В {month_name.lower()} трат нет."

    total = sum(e["amount"] for e in expenses)

    by_category: dict[str, float] = {}
    for e in expenses:
        by_category[e["category"]] = by_category.get(e["category"], 0) + e["amount"]

    lines = [
        f"📊 <b>Отчёт: {month_name}</b>",
        f"Итого: <b>{fmt_amount(total)}</b> ({len(expenses)} трат)",
        "",
    ]

    for cat, amount in sorted(by_category.items(), key=lambda x: -x[1]):
        label = CATEGORIES.get(cat, cat)
        pct = amount / total * 100
        lines.append(f"{label}  <b>{fmt_amount(amount)}</b>  ({pct:.1f}%)")

    return "\n".join(lines)


def fmt_day_report(expenses: list[dict], year: int, month: int, day: int) -> str:
    date_str = f"{day} {MONTHS_RU[month].lower()} {year}"

    if not expenses:
        return f"📅 {date_str} — трат нет."

    total = sum(e["amount"] for e in expenses)

    by_category: dict[str, float] = {}
    for e in expenses:
        by_category[e["category"]] = by_category.get(e["category"], 0) + e["amount"]

    lines = [
        f"📅 <b>Отчёт: {date_str}</b>",
        f"Итого: <b>{fmt_amount(total)}</b> ({len(expenses)} трат)",
        "",
    ]

    for cat, amount in sorted(by_category.items(), key=lambda x: -x[1]):
        label = CATEGORIES.get(cat, cat)
        pct = amount / total * 100
        lines.append(f"{label}  <b>{fmt_amount(amount)}</b>  ({pct:.1f}%)")

    return "\n".join(lines)


MONTHS_RU_GENITIVE = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
    5: "мая", 6: "июня", 7: "июля", 8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря",
}


def fmt_detail_report(expenses: list[dict], year: int, month: int) -> str:
    month_name = f"{MONTHS_RU[month]} {year}"

    if not expenses:
        return f"📋 В {month_name.lower()} трат нет."

    total = sum(e["amount"] for e in expenses)

    by_day: dict[int, list[dict]] = {}
    for e in expenses:
        day = int(e["created_at"][8:10])
        by_day.setdefault(day, []).append(e)

    lines = [
        f"📋 <b>Детальный отчёт: {month_name}</b>",
        f"Итого: <b>{fmt_amount(total)}</b> ({len(expenses)} трат)",
    ]

    for day in sorted(by_day, reverse=True):
        day_expenses = by_day[day]
        day_total = sum(e["amount"] for e in day_expenses)
        lines.append("")
        lines.append(f"── <b>{day} {MONTHS_RU_GENITIVE[month]}</b> ──")
        for e in day_expenses:
            label = CATEGORIES.get(e["category"], e["category"])
            desc = f" — {e['description']}" if e.get("description") else ""
            lines.append(f"{label}  <b>{fmt_amount(e['amount'])}</b>{desc}")
        lines.append(f"За день: <b>{fmt_amount(day_total)}</b>")

    return "\n".join(lines)


def fmt_history(expenses: list[dict]) -> str:
    if not expenses:
        return "Трат пока нет."

    lines = ["🧾 <b>Последние траты:</b>", ""]
    for e in expenses:
        label = CATEGORIES.get(e["category"], e["category"])
        desc = f" — {e['description']}" if e.get("description") else ""
        date = e["created_at"][:10]
        lines.append(f"{date}  {label}  <b>{fmt_amount(e['amount'])}</b>{desc}  /del{e['id']}")

    return "\n".join(lines)
