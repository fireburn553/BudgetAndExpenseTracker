import sqlite3

def get_connection():
    """Return a connection to the SQLite database."""
    return sqlite3.connect("budget_tracker.db")

def create_database():
    """Create a SQLite database and tables for the budget tracker."""

    conn = get_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS income (
        income_id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        amount REAL NOT NULL,
        month TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS expense_category (
        expense_category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS payment_method (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        method_name TEXT UNIQUE NOT NULL
    );

    -- Insert payment methods after table creation
    INSERT OR IGNORE INTO payment_method (method_name)
    VALUES
        ('Cash'),
        ('Credit Card'),
        ('Debit Card'),
        ('Mobile Payment / Cashless');

    CREATE TABLE IF NOT EXISTS expenses (
        expenses_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        store TEXT NOT NULL,
        details TEXT,
        amount REAL NOT NULL,
        category_id INTEGER NOT NULL,
        payment_method_id INTEGER NOT NULL,
        FOREIGN KEY (category_id) REFERENCES expense_category(expense_category_id),
        FOREIGN KEY (payment_method_id) REFERENCES payment_method(payment_id)
    );
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    print("Database and tables created successfully.")
