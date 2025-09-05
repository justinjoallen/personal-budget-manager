import sqlite3
import csv
from datetime import datetime
 
class BudgetManagerDB:
    def __init__(self, db_name="budget.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
        self.patch_table()
 
    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL CHECK(amount > 0),
                    note TEXT
                )
            """)
 
    def patch_table(self):
        cursor = self.conn.execute("PRAGMA table_info(expenses)")
        columns = [col[1] for col in cursor.fetchall()]
 
        if 'date' not in columns:
            # Add column without default
            self.conn.execute("ALTER TABLE expenses ADD COLUMN date TEXT")
 
            # Update existing rows with current timestamp
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.conn.execute("UPDATE expenses SET date = ?", (now,))
 
    def add_expense(self, category, amount, note=""):
        if not category or amount <= 0:
            raise ValueError("Invalid category or amount.")
        with self.conn:
            self.conn.execute(
                "INSERT INTO expenses (category, amount, note, date) VALUES (?, ?, ?, datetime('now', 'localtime'))",
                (category, amount, note)
            )
 
    def view_expenses(self):
        cursor = self.conn.execute("SELECT id, category, amount, note, date FROM expenses")
        return cursor.fetchall()
 
    def total_by_category(self):
        cursor = self.conn.execute("""
            SELECT category, SUM(amount) FROM expenses GROUP BY category
        """)
        return cursor.fetchall()
 
    def delete_expense(self, expense_id):
        with self.conn:
            self.conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
 
    def update_expense(self, expense_id, category, amount, note):
        with self.conn:
            self.conn.execute("""
                UPDATE expenses SET category = ?, amount = ?, note = ? WHERE id = ?
            """, (category, amount, note, expense_id))
 
    def filter_expenses(self, category=None, start_date=None, end_date=None):
        query = "SELECT id, category, amount, note, date FROM expenses WHERE 1=1"
        params = []
        if category:
            query += " AND category = ?"
            params.append(category)
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        cursor = self.conn.execute(query, params)
        return cursor.fetchall()
 
    def export_to_csv(self, filename="expenses.csv"):
        rows = self.view_expenses()
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Category", "Amount", "Note", "Date"])
            writer.writerows(rows)