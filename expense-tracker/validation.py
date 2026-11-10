def validate_expense(item: object) -> dict:
    """Проверить одну запись из файла. При проблеме бросает ValueError."""
    if not isinstance(item, dict):
        raise ValueError(f"запись должна быть объектом, а не {type(item).__name__}")
    for field in ("title", "amount", "category"):
        if field not in item:
            raise ValueError(f"нет поля '{field}'")
    if not isinstance(item["title"], str) or not item["title"].strip():
        raise ValueError("title должен быть непустой строкой")
    amount = item["amount"]
    # bool в Python — подкласс int, поэтому True прошёл бы как число
    if isinstance(amount, bool) or not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError("amount должен быть положительным числом")
    if not isinstance(item["category"], str) or not item["category"].strip():
        raise ValueError("category должна быть непустой строкой")
    return item