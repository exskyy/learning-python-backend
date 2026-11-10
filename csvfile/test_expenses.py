from pathlib import Path
import csv

directory = Path('C:/BACKEND/учусь')
file = directory / 'expenses.csv'

def import_expenses(csv_path: Path | str) -> list[dict]:
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    if not path.is_file():
        raise IsADirectoryError(f"Ожидался файл, а не папка: {path}")
    if path.stat().st_size == 0:
        raise ValueError(f"Файл пустой: {path}")

    expenses = []

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)

        # первая строка — заголовок
        header = next(reader, None)   # None — если файл из одной пустой строки
        if header is None:
            raise ValueError(f"В файле нет заголовка: {path}")

        # проверь, что колонки те, что ждём
        expected = ["date", "category", "amount", "note"]
        if [h.strip() for h in header] != expected:
            raise ValueError(
                f"Неверные колонки. Ожидались {expected}, получили {header}"
            )

        for row_num, row in enumerate(reader, start=2):   # 2 — т.к. заголовок строка 1
            # пустые строки в конце файла — пропускаем
            if not row or all(cell.strip() == "" for cell in row):
                continue

            if len(row) != len(expected):
                raise ValueError(
                    f"Строка {row_num}: ожидалось {len(expected)} колонок, "
                    f"найдено {len(row)}: {row}"
                )

            date, category, amount_str, note = (cell.strip() for cell in row)

            try:
                amount = float(amount_str)
            except ValueError:
                raise ValueError(
                    f"Строка {row_num}: сумма не число: {amount_str!r}"
                ) from None

            expenses.append({
                "date": date,
                "category": category,
                "amount": amount,
                "note": note,
            })
    return expenses

sum = 0
for e in import_expenses(file):
    sum += e["amount"]
print(f"Всего расходов: {sum:.2f} руб за {len(import_expenses(file))} записей")