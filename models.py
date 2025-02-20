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
        SELECT e.expenses_id, e.date, e.store, e.details, e.amount, c.category_name, p.method_name
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
    """Add a new expense category to the database, ensuring it does not already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Check if category already exists
    cursor.execute(
        "SELECT 1 FROM expense_category WHERE category_name = ?",
        (category_name,)
    )
    existing_category = cursor.fetchone()

    if existing_category:
        print(f"Category '{category_name}' already exists.")  # Handle as needed
    else:
        cursor.execute(
            """
            INSERT INTO expense_category (category_name)
            VALUES (?)
            """,
            (category_name,)
        )
        conn.commit()
        print(f"Category '{category_name}' added successfully.")

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

def update_category_name(category_id, category_name):
    """Update the name of an expense category only if it exists."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM expense_category WHERE expense_category_id = ?", (category_id,))
    existing_category = cursor.fetchone()

    if existing_category:
        cursor.execute(
            "UPDATE expense_category SET category_name = ? WHERE expense_category_id = ?",
            (category_name, category_id)
        )
        conn.commit()
        print(f"Category No. {category_id} updated successfully.")
    else:
        print(f"Category No. {category_id} does not exist.")

    conn.close()

def delete_category(category_id):
    """Delete an expense category from the database only if it exists."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM expense_category WHERE expense_category_id = ?", (category_id,))
    existing_category = cursor.fetchone()

    if existing_category:
        cursor.execute("DELETE FROM expense_category WHERE expense_category_id = ?", (category_id,))
        conn.commit()
        print(f"Category ID {category_id} deleted successfully.")
    else:
        print(f"Category ID {category_id} does not exist.")

    conn.close()

def update_expenses (expenses_id, date, store, details, amount, category_id, payment_method_id):
    """Update an expense record in the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE expenses
        SET date = ?, store = ?, details = ?, amount = ?, category_id = ?, payment_method_id = ?
        WHERE expenses_id = ?
        """,
        (date, store, details, amount, category_id, payment_method_id, expenses_id)
    )

    conn.commit()
    conn.close()

def delete_expense(expenses_id):   
    """Delete an expense record from the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM expenses
        WHERE expenses_id = ?
        """,
        (expenses_id,)
    )

    conn.commit()
    conn.close()

def select_category(category_name):
    """Select an expense category from the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT expense_category_id
        FROM expense_category
        WHERE category_name = ?
        """,
        (category_name,)
    )

    category_id = cursor.fetchone()
    conn.close()
    return category_id[0] if category_id else 0  # Return 0 if category does not exist

def select_payment_method(method_name):
    """Select a payment method from the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT payment_id
        FROM payment_method
        WHERE method_name = ?
        """,
        (method_name,)
    )

    method_id = cursor.fetchone()
    conn.close()
    return method_id[0] if method_id else 0  # Return 0 if payment method does not exist