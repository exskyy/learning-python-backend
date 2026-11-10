from pathlib import Path
import json
import csv

BASE_DIR = Path(__file__).parent          # папка, где лежит normalize.py
JSON_FILE = BASE_DIR / "normalized.json"
CSV_FILE = BASE_DIR / "normalized.csv"

RAW = [
    {"id": 1, "title": " Кофе ", "amount": "150,50", "category": {"name": "Еда"}, "date": "2026-11-01"},
    {"id": 2, "title": "Такси", "amount": 320, "category": {"name": "Транспорт"}, "date": "2026-11-02"},
    {"id": 2, "title": "Такси", "amount": 320, "category": {"name": "Транспорт"}, "date": "2026-11-02"},  # дубль
    {"id": 3, "title": "Книга", "amount": None, "category": None, "date": "2026-11-03"},  # нет суммы
    {"id": 4, "title": "Обед", "amount": "abc", "category": {"name": "еда"}},             # сумма не число
    {"title": "Без id", "amount": 10},                                                    # нет id
    {"id": 5, "title": "  ", "amount": 99, "category": {"name": "Разное"}, "date": ""},   # пустое название и дата
]
def normalize_record(raw):
    try:
        record_id = int(raw["id"])
        amount = float(str(raw["amount"]).replace(",", "."))
    except (KeyError, TypeError, ValueError):
        return None

    title = (raw.get("title") or "").strip() or "Без названия"
    category = ((raw.get("category") or {}).get("name") or "").strip() or "Без категории"
    date = (raw.get("date") or "").strip() or None

    return {
        "id": record_id,
        "title": title,
        "amount": round(amount, 2),
        "category": category.capitalize(),
        "date": date
    }

def normalize_all(raw_items, normalizer, key_fields):
    seen = set()
    result = []
    skipped = 0
    duplicates = 0

    for raw in raw_items:
        normalized = normalizer(raw)
        if normalized is None:
            skipped += 1
            continue

        key = tuple(normalized[field] for field in key_fields)
        if key in seen:
            duplicates += 1
            continue

        seen.add(key)
        result.append(normalized)

    print(f"Получено: {len(raw_items)}, оставлено: {len(result)}, "
          f"пропущено (нет обязательных полей): {skipped}, дубликатов: {duplicates}")
    return result

def save_json(records, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=4)


def save_csv(records, path, fields):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    records = normalize_all(RAW, normalize_record, ("id",))
    save_json(records, JSON_FILE)
    save_csv(records, CSV_FILE, fields=["id", "title", "amount", "category", "date"])
    print("Сохранено:", JSON_FILE, "и", CSV_FILE)
