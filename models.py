from datetime import datetime
from database import get_connection


month = datetime.now().strftime('%B')  # Get the current month as a string

def add_income(income_source, amount, month):
    """Add a new income record to the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO income (source, amount, month)
        VALUES (?, ?, ?)
        """,
        (income_source, amount, month)
    )

    conn.commit()
    conn.close()

def add_expense(date, store, details, amount, category_id, payment_method_id):
    """Add a new expense record to the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO expenses (date, store, details, amount, category_id, payment_method_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (date, store, details, amount, category_id, payment_method_id)
    )

    conn.commit()
    conn.close()

def view_expenses():
    """Return a list of all expenses for the current month from the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT e.date, e.store, e.details, e.amount, c.category_name, p.method_name
        FROM expenses e 
        JOIN expense_category c ON e.category_id = c.expense_category_id
        JOIN payment_method p ON e.payment_method_id = p.payment_id
        WHERE strftime('%Y-%m', e.date) = strftime('%Y-%m', 'now')
        ORDER BY e.date;
        """
    )

    results = cursor.fetchall()  # Fetch all results
    conn.close()
    return results

def view_quick_expenses():
    """Return the total expenses for the current month."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT SUM(amount) AS total_expenses
        FROM expenses
        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now');
        """
    )

    total = cursor.fetchone()[0]  # Fetch single result
    conn.close()
    return total if total else 0  # Return 0 if no expenses

def view_income():
    """Return the total actual income for the current month."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT SUM(amount) FROM income WHERE month = ?;
        """, (month,)
    )

    total_income = cursor.fetchone()[0]  # Fetch single result
    conn.close()
    return total_income if total_income else 0  # Return 0 if no income records

def add_expense_category(category_name):
    """Add a new expense category to the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO expense_category (category_name)
        VALUES (?)
        """,
        (category_name,)
    )

    conn.commit()
    conn.close()

def view_expenses_category():
    """Return a list of all expense categories."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM expense_category;
        """
    )

    results = cursor.fetchall()  # Fetch all results
    conn.close()
    return results

def view_payment_method():
    """Return a list of all payment methods."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM payment_method;
        """
    )

    results = cursor.fetchall()  # Fetch all results
    conn.close()
    return results

def total_expenses_per_category():
    """Return the total expenses for each category."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT c.category_name, SUM(e.amount) AS total_expenses
        FROM expenses e
        JOIN expense_category c ON e.category_id = c.expense_category_id
        WHERE strftime('%Y-%m', e.date) = strftime('%Y-%m', 'now')
        GROUP BY c.category_name;
        """
    )

    results = cursor.fetchall()  # Fetch all results
    conn.close()
    return results