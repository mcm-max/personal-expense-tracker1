import sqlite3
from datetime import datetime

DB_NAME = "expenses.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_expense(Title, category, amount):
    conn = connect_db()
    cursor = conn.cursor()

    date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT INTO expenses (Title, category, amount, date)
        VALUES (?, ?, ?, ?)
    """, (Title, category, amount, date))

    conn.commit()
    conn.close()

    print("Expense added successfully!")


def view_expenses():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, Title, category, amount, date
        FROM expenses
        ORDER BY id DESC
    """)

    expenses = cursor.fetchall()
    conn.close()

    if len(expenses) == 0:
        print("No expenses found.")
        return

    print("\n--- Expenses ---")

    for expense in expenses:
        print(
            f"ID: {expense[0]} | "
            f"{expense[1]} | "
            f"{expense[2]} | "
            f"${expense[3]:.2f} | "
            f"{expense[4]}"
        )


def category_summary():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    results = cursor.fetchall()
    conn.close()

    if len(results) == 0:
        print("No expenses found.")
        return

    print("\n--- Spending by Category ---")

    for category, total in results:
        print(f"{category}: ${total:.2f}")


def total_spending():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses")

    total = cursor.fetchone()[0]
    conn.close()

    if total is None:
        total = 0

    print(f"\nTotal Spending: ${total:.2f}")


def delete_expense(expense_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("Expense deleted.")
    else:
        print("Expense ID not found.")

    conn.close()


def main():
    create_table()

    while True:
        print("\nPersonal Expense Tracker")
        print("------------------------")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Spending by Category")
        print("4. View Total Spending")
        print("5. Delete Expense")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            Title = input("Enter Title: ")
            category = input("Enter category: ")

            try:
                amount = float(input("Enter amount: $"))

                if amount < 0:
                    print("Amount cannot be negative.")
                    continue

                add_expense(Title, category, amount)

            except ValueError:
                print("Please enter a valid amount.")

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            category_summary()

        elif choice == "4":
            total_spending()

        elif choice == "5":
            try:
                expense_id = int(input("Enter the expense ID: "))
                delete_expense(expense_id)

            except ValueError:
                print("Please enter a valid ID.")

        elif choice == "6":
            print("Goodbye Have a great day!")
            break

        else:
            print("Please choose a number between 1 and 6.")


if __name__ == "__main__":
    main()