from cli import add_expense, show_expenses, show_totals, show_report, ask_period
from services import build_report
from storage import load_expenses

def main() -> None:
    expenses = load_expenses()
    while True:
        print("\n1. Добавить расход")
        print("2. Показать расходы")
        print("3. Показать итоги")
        print("4. Показать отчет за период")
        print("5. Выход")
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            show_totals(expenses)
        elif choice == "4":
            show_report(build_report(expenses, *ask_period()))
        elif choice == "5":
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nДо свидания!")