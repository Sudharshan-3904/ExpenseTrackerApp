import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import getpass


class Authenticator:
    def __init__(self):
        self.conn = sqlite3.connect('expense_tracker.db')

    def create_connection(self):
        self.conn = sqlite3.connect('expense_tracker.db')
        return self.conn

    def create_tables(self):
        self.create_connection()
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()
        self.conn.close()

    def register_user(self, username, password):
        self.create_connection()
        cursor = self.conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.conn.commit()
            print("User  registered successfully.")
        except sqlite3.OperationalError:
            self.create_tables()
        except sqlite3.IntegrityError:
            print("Username already exists.")
        finally:
            self.conn.close()

    def authenticate_user(self, username, password):
        self.create_connection()
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        self.conn.close()
        return user

class Expense:
    def __init__(self, user_id, amount, category, date):
        self.user_id = user_id 
        self.amount = amount
        self.category = category
        self.date = date


class ExpenseTracker:
    def __init__(self):
        self.conn = Authenticator().create_connection()
        self.cursor = self.conn.cursor()

    def add_expense(self, user_id, amount, category, date):
        self.cursor.execute('INSERT INTO expenses (user_id, amount, category, date) VALUES (?, ?, ?, ?)', 
                    (user_id, amount, category, date))
        self.conn.commit()

    def get_expenses(self, user_id, start_date, end_date):
        self.cursor.execute('SELECT amount, category, date FROM expenses WHERE user_id = ? AND date BETWEEN ? AND ?', 
                    (user_id, start_date, end_date))
        self.expenses = self.cursor.fetchall()

    def plot_expenses(self):
        dself.get_expenses()
        categories = {}
        for amount, category, _ in self.expenses:
            if category in categories:
                categories[category] += amount
            else:
                categories[category] = amount

        plt.bar(categories.keys(), categories.values())
        plt.xlabel('Categories')
        plt.ylabel('Amount Spent')
        plt.title('Expenses by Category')
        plt.show()


thing = Authenticator()
thing.register_user("hello", "hi")