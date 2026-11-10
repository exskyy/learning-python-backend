import json
import shutil
from datetime import datetime
from pathlib import Path
from validation import validate_expense

DATA_FILE = Path(__file__).parent / "expenses.json"

def backup_path(path: Path) -> Path:
    """Имя для копии с меткой времени, чтобы новая копия не затирала старую."""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return path.with_name(f"{path.name}.{stamp}.bak")


def backup_broken_file(path: Path) -> Path:
    """Переименовать испорченный файл в .bak, чтобы не затереть его при сохранении."""
    backup = backup_path(path)
    path.replace(backup)
    return backup


def load_expenses() -> list[dict]:
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []  # первый запуск — это нормально
    except json.JSONDecodeError as e:
        backup = backup_broken_file(DATA_FILE)
        print(f"Файл повреждён (строка {e.lineno}, столбец {e.colno}): {e.msg}.")
        print(f"Копия сохранена в {backup.name}, начинаю с пустого списка.")
        return []

    if not isinstance(data, list):
        backup = backup_broken_file(DATA_FILE)
        print("В файле ожидался список записей.")
        print(f"Копия сохранена в {backup.name}, начинаю с пустого списка.")
        return []

    valid = []
    skipped = 0
    for i, item in enumerate(data, start=1):
        try:
            expense = validate_expense(item)
        except ValueError as e:
            print(f"Запись №{i} пропущена: {e}")
            skipped += 1
            continue
        expense["category"] = expense["category"].strip().lower()
        valid.append(expense)

    if skipped:
        # При следующем сохранении пропущенные записи исчезнут из файла,
        # поэтому заранее сохраняем исходный файл целиком.
        backup = backup_path(DATA_FILE)
        shutil.copy2(DATA_FILE, backup)
        print(f"Пропущено записей: {skipped}. Исходный файл сохранён в {backup.name}.")
    return valid


def save_expenses(expenses: list[dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=4)
