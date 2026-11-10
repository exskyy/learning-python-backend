from services import totals_by_category
from storage import save_expenses
from datetime import date
import math

def ask_amount() -> float:
    while True:
        raw = input("Введите сумму: ").strip().replace(",", ".")
        try:
            amount = float(raw)
        except ValueError:
            print("Введено некорректное число")
            continue

        if not math.isfinite(amount) or amount <= 0:
            print("Сумма должна быть положительным числом")
            continue

        return amount


def ask_nonempty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Значение не может быть пустым")

def ask_date(prompt: str) -> str:
    while True:
        raw = input(prompt).strip()
        try:
            parsed = date.fromisoformat(raw)
        except ValueError:
            print("Дата должна быть реальной и в формате ГГГГ-ММ-ДД, например 2026-11-03")
            continue
        return parsed.isoformat()

def ask_period() -> tuple[str, str]:
    start = ask_date("Введите дату начала периода (ГГГГ-ММ-ДД): ")
    end = ask_date("Введите дату конца периода (ГГГГ-ММ-ДД): ")
    if start > end:
        print("Дата начала периода не может быть позже даты конца периода")
        return ask_period()
    return start, end

def show_report(report) -> None:
    print(f"Отчет за период с {report['start']} по {report['end']}")
    print("Итоги по категориям:")
    for category, amount in report["totals"].items():
        print(f"{category}: {amount:.2f}")
    print("Расходы:")
    show_expenses(report["expenses"])

def show_expenses(expenses: list[dict]) -> None:
    if not expenses:
        print("Расходов пока нет")
        return

    for number, expense in enumerate(expenses, start=1):
        title = expense["title"]
        amount = expense["amount"]
        category = expense["category"]
        print(f"{number}. {title} - {amount:.2f} ({category})")

    total = sum(expense["amount"] for expense in expenses)
    print(f"Всего: {total:.2f}")

def show_totals(expenses: list[dict]) -> None:
    if not expenses:
        print("Расходов пока нет")
        return

    totals = totals_by_category(expenses)
    sorted_totals = sorted(totals.items(), key=lambda x: x[1], reverse=True)

    for category, amount in sorted_totals:
        print(f"{category}: {amount:.2f}")

    print(f"Всего: {sum(totals.values()):.2f}")

def add_expense(expenses: list[dict]) -> None:
    title = ask_nonempty("Введите название расхода: ")
    amount = ask_amount()
    category = ask_nonempty("Введите категорию: ").lower()
    date = ask_date("Введите дату (ГГГГ-ММ-ДД): ")

    expense = {
        "title": title,
        "amount": amount,
        "category": category,
        "date": date,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print("Добавлено!")