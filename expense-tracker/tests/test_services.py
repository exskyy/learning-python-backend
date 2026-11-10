from services import totals_by_category


def test_sum_by_category():
    expenses = [
        {"title": "a", "amount": 10, "category": "еда"},
        {"title": "b", "amount": 5, "category": "еда"},
    ]
    result = totals_by_category(expenses)
    assert result == {"еда": 15}