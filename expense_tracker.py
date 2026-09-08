import sqlite3
from datetime import datetime

DB_NAME = "expenses.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount >= 0),
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_expense(description, category, amount):
    conn = connect_db()
    cursor = conn.cursor()

    date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT INTO expenses (description, category, amount, date)
        VALUES (?, ?, ?, ?)
    """, (description, category, amount, date))

    conn.commit()
    conn.close()

    print("Expense added successfully.")


def view_expenses():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, description, category, amount, date
        FROM expenses
        ORDER BY date DESC, id DESC
    """)

    expenses = cursor.fetchall()

    if not expenses:
        print("\nNo expenses found.")
    else:
        print("\n--- All Expenses ---")

        for expense in expenses:
            print(
                f"ID: {expense[0]} | "
                f"{expense[1]} | "
                f"{expense[2]} | "
                f"${expense[3]:.2f} | "
                f"{expense[4]}"
            )

    conn.close()


def view_category_summary():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    results = cursor.fetchall()

    if not results:
        print("\nNo expenses found.")
    else:
        print("\n--- Spending by Category ---")

        for category, total in results:
            print(f"{category}: ${total:.2f}")

    conn.close()


def view_total_spending():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses")

    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    print(f"\nTotal spending: ${total:.2f}")

    conn.close()


def delete_expense(expense_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    conn.commit()

    if cursor.rowcount > 0:
        print("Expense deleted successfully.")
    else:
        print("Expense ID not found.")

    conn.close()


def menu():
    create_tables()

    while True:
        print("\n==========================")
        print("    PERSONAL EXPENSE TRACKER")
        print("==========================")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Spending by Category")
        print("4. View Total Spending")
        print("5. Delete Expense")
        print("6. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            description = input("Description: ").strip()
            category = input("Category: ").strip()

            if not description or not category:
                print("Description and category cannot be empty.")
                continue

            try:
                amount = float(input("Amount: $"))

                if amount < 0:
                    print("Amount cannot be negative.")
                    continue

                add_expense(description, category, amount)

            except ValueError:
                print("Please enter a valid number.")

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            view_category_summary()

        elif choice == "4":
            view_total_spending()

        elif choice == "5":
            try:
                expense_id = int(input("Enter expense ID to delete: "))
                delete_expense(expense_id)

            except ValueError:
                print("Please enter a valid ID number.")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please choose 1-6.")


if __name__ == "__main__":
    menu()