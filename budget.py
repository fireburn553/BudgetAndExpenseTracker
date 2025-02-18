import datetime
from tabulate import tabulate
from models import total_expenses_per_category, view_payment_method, view_expenses_category, add_expense, view_expenses, view_quick_expenses, view_income, add_income, add_expense_category
from database import create_database


def menu():
    create_database()

    while True:
        total_expenses = view_quick_expenses()
        month = datetime.datetime.now()
        total_income = view_income()    

        print(f"Quick View of Budget and Expenses for the Month of {month.strftime("%B %Y")}")
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expenses: ${total_expenses:.2f}")
        print(f"Remaining Budget: ${total_income - total_expenses:.2f}")
        

        print("\nBudget Tracker | Main Menu")
        print("[1] Add Expense Category")
        print("[2] View Expenses")
        print("[3] Record Expenses")
        print("[4] Set Income Budget")
        print("[5] View Total Expenses per Category")
        print("[6] View Expenses Category")
        print("[7] Exit")

        choice = input("Choose an option: ")
        #DONE
        if choice == "1":
            category_name = input("Enter expense category name: ")
            add_expense_category(category_name)
            print("Expense category added successfully.")

        #DONE
        elif choice == "2":
           print("Expenses for the Month of", month.strftime("%B %Y"))
           headers = ["Date", "Store", "Details", "Amount", "Category", "Payment Method"]
           formatted_result =[
               [row[0], row[1], row[2], f"${row[3]:,.2f}", row[4], row[5]]
               for row in view_expenses()
           ]
           print(tabulate(formatted_result, headers=headers, tablefmt="grid"))

        #DONE
        elif choice == "3":
            expense_date = input("Enter date (YYYY-MM-DD): ")
            store = input("Enter store name: ")
            details = input("Enter details: ")
            amount = float(input("Enter amount: "))
            print("Expense Categories:")
            for row in view_expenses_category():
                print(row[0], row[1])
            category_id = int(input("Enter category ID: "))
            print("Payment Methods: (Cash, Credit Card, Debit Card, Mobile Payment)")
            for row in view_payment_method():
                print(row[0], row[1])
            payment_method_id = int(input("Enter payment method ID: "))
            add_expense(expense_date, store, details, amount, category_id, payment_method_id)
       
        #DONE 
        elif choice == "4":
            source = input("Enter income source: ")
            amount = float(input("Enter amount: "))
            print(source, amount, month.strftime("%B"))
            add_income(source, amount, month.strftime("%B"))
            print("Income added successfully.")
        #DONE
        elif choice == "5":
            print("Total Expenses per Category:")
            headers = ["Category", "Total Expenses"]
            print(tabulate(total_expenses_per_category(), headers=headers, tablefmt="grid"))
        
        #DONE
        elif choice == "6":
            print("Expense Categories:")
            headers = ["No.","Category"]
            print(tabulate(view_expenses_category(), headers=headers, tablefmt="grid"))
            
        elif choice == "7":
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    menu()
