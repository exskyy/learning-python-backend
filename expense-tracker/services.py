def totals_by_category(expenses: list[dict]) -> dict[str, float]:
    totals: dict[str, float] = {}
    for expense in expenses:
        amount = expense["amount"]
        category = expense["category"]
        totals[category] = totals.get(category, 0) + amount
    return totals

def filter_by_period(expenses: list[dict], start: str, end: str) -> list[dict]:
    return [expense for expense in expenses if expense.get("date") and start <= expense["date"] <= end]

def build_report(expenses: list[dict], start: str, end: str) -> dict:
    filtered_expenses = filter_by_period(expenses, start, end)
    totals = totals_by_category(filtered_expenses)
    return {
        "start": start,
        "end": end,
        "totals": totals,
        "expenses": filtered_expenses,
    }