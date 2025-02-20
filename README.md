# 📊 Budget and Expense Tracker

## 📝 Overview

The **Budget and Expense Tracker** is a **Command-Line Interface (CLI) application** built with **Python** and **SQLite**. It is designed to help users efficiently manage their financial transactions by adding, viewing, editing, and deleting expenses. The system ensures data validation, proper data storage, and retrieval from an integrated relational database.

This project aims to strengthen my understanding of **Python programming, database management, and data validation techniques** while building a practical financial tracking system.

### 🔹 Features

✅ **Expense Management** – Add, view, edit, and delete expenses.

✅ **Expense Categories** – Categorize expenses for better tracking.

✅ **Data Validation** – Ensures only valid user inputs are accepted.

✅ **SQLite Database Integration** – Stores and manages financial records securely.

✅ **Tabular Data Display** – Uses the `tabulate` library for clear presentation.

### 🎥 Software Demo

[Software Demo Video](http://youtube.link.goes.here)

---

## 🛢 Relational Database

The project uses an **SQLite relational database** to store and manage financial data efficiently.

### 📋 Database Structure

The database consists of the following tables:

1. **income**

   - `income_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
   - `source` (TEXT, NOT NULL)
   - `amount` (REAL, NOT NULL)
   - `month` (TEXT, NOT NULL)

2. **expense_category**

   - `expense_category_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
   - `category_name` (TEXT, UNIQUE, NOT NULL)

3. **payment_method**

   - `payment_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
   - `method_name` (TEXT, UNIQUE, NOT NULL)

4. **expenses**
   - `expenses_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
   - `date` (TEXT, NOT NULL)
   - `store` (TEXT, NOT NULL)
   - `details` (TEXT, NULL)
   - `amount` (REAL, NOT NULL)
   - `category_id` (INTEGER, NOT NULL, FOREIGN KEY references `expense_category(expense_category_id)`)
   - `payment_method_id` (INTEGER, NOT NULL, FOREIGN KEY references `payment_method(payment_id)`)

Additionally, the `payment_method` table is pre-populated with common payment methods (`Cash`, `Credit Card`, `Debit Card`, `Mobile Payment / Cashless`).

---

## 💻 Development Environment

- **Programming Language:** Python 3.13.1
- **Database:** SQLite3
- **Libraries Used:**
  - `sqlite3` – for database interaction
  - `tabulate` – for formatted table display
  - `datetime` – for date handling

---

## 🌐 Useful Websites

- [Python Official Documentation](https://docs.python.org/3/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Tabulate Library](https://pypi.org/project/tabulate/)
- [Introduction to SQLite | Geeks for Geeks](https://www.geeksforgeeks.org/introduction-to-sqlite/)
- [Python Tutorial | W3Schools](https://www.w3schools.com/python/default.asp)

---

## 🚀 Future Work

🔹 **User Authentication** – Implement user accounts for personalized tracking.

🔹 **Income Tracking** – Add an income management feature.

🔹 **Report Generation** – Generate monthly financial reports.

🔹 **Graphical User Interface (GUI)** – Convert CLI to a GUI application.

---
