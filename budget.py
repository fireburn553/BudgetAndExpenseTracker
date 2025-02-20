import datetime
from tabulate import tabulate
from models import select_payment_method, select_category, delete_expense, update_expenses, delete_category,update_category_name,total_expenses_per_category, view_payment_method, view_expenses_category, add_expense, view_expenses, view_quick_expenses, view_income, add_income, add_expense_category
from database import create_database


def menu():
    create_database() # Create the database if it does not exist and initialize the tables

    while True:
        # Display a quick view
        total_expenses = view_quick_expenses() 
        month = datetime.datetime.now()
        total_income = view_income()    
        print()
        print("--------------------------------------------------------------------------") 
        print(f"Quick View of Budget and Expenses for the Month of {month.strftime("%B %Y")}")
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expenses: ${total_expenses:.2f}")
        print(f"Remaining Budget: ${total_income - total_expenses:.2f}")
        
        # Display the main menu
        print("\nBudget Tracker | Main Menu")
        print("Expense")
        print("[1] View Expenses")
        print("[2] Record Expenses")
        print("[3] View Total Expenses per Category")        
        print()
        print("Budget")
        print("[4] Set Income Budget")
        print()
        print("Expense Category")
        print("[5] Add Expense Category")
        print("[6] View Expenses Category")
        print("EXIT") 
        print("[7] Exit")
        print("--------------------------------------------------------------------------")
        
        choice = input("Choose an option: ")
        print("--------------------------------------------------------------------------")

        if choice == "1": # View Expenses
            print()
            print("Expenses for the Month of", month.strftime("%B %Y")) 

            if len(view_expenses()) == 0: 
                print("No expenses available.")
                input("Press Enter to continue.")
            else:
                headers = ["No.", "Date", "Store", "Details", "Amount", "Category", "Payment Method"]
                formatted_result = [
                    [index + 1, row[1], row[2], row[3], f"${row[4]:,.2f}", row[5], row[6]]
                    for index, row in enumerate(view_expenses())
                ]
                print(tabulate(formatted_result, headers=headers, tablefmt="grid"))

                print("[1] Edit Expense")
                print("[2] Delete Expense")
                print("[3] Back to Main Menu")

                choice = input("Choose an option: ").strip()

                if choice == "1":
                    print("\nEdit Expense")
                    print("Expenses:")
                    print(tabulate(formatted_result, headers=headers, tablefmt="grid"))

                    # Validate expense selection
                    while True:
                        try:
                            expenses_id = int(input("Enter expense number: "))
                            if 1 <= expenses_id <= len(formatted_result):
                                break
                            print("Invalid selection. Choose a valid expense number.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")

                    selected_expense = formatted_result[expenses_id - 1][1:]
                    expense_id = view_expenses()[expenses_id - 1][0]

                    updated_values = list(selected_expense)
                    fields = ["Date", "Store", "Details", "Amount", "Category", "Payment Method"]

                    for i in range(len(fields)):
                        print(f"\nEdit {fields[i]}? Y/N")
                        print(f"Current value: {updated_values[i]}")  # Show current value
                        choice = input("Enter choice: ").strip().lower()

                        if choice == "y":
                            if fields[i] == "Date":
                                while True:
                                    new_value = input(f"Enter updated {fields[i]} (YYYY-MM-DD): ").strip()
                                    try:
                                        datetime.datetime.strptime(new_value, "%Y-%m-%d")  # Validate date format
                                        break
                                    except ValueError:
                                        print("Invalid date format. Please enter a valid date (YYYY-MM-DD).")

                            elif fields[i] == "Amount":
                                while True:
                                    try:
                                        new_value = float(input(f"Enter updated {fields[i]}: "))
                                        if new_value > 0:
                                            break
                                        print("Amount must be a positive number.")
                                    except ValueError:
                                        print("Invalid input. Please enter a valid number.")

                            elif fields[i] == "Category":
                                print("\nExpense Categories:")
                                category_list = view_expenses_category()
                                for row in category_list:
                                    print(f"{row[0]} - {row[1]}")

                                valid_category_ids = [row[0] for row in category_list]  # Get valid category IDs
                                while True:
                                    try:
                                        new_value = int(input(f"Enter updated {fields[i]} (ID): "))
                                        if new_value in valid_category_ids:
                                            break
                                        print("Invalid category ID. Please enter a valid ID from the list.")
                                    except ValueError:
                                        print("Invalid input. Please enter a number.")

                            elif fields[i] == "Payment Method":
                                print("\nPayment Methods:")
                                payment_list = view_payment_method()
                                for row in payment_list:
                                    print(f"{row[0]} - {row[1]}")

                                valid_payment_ids = [row[0] for row in payment_list]  # Get valid payment method IDs
                                while True:
                                    try:
                                        new_value = int(input(f"Enter updated {fields[i]} (ID): "))
                                        if new_value in valid_payment_ids:
                                            break
                                        print("Invalid payment method ID. Please enter a valid ID from the list.")
                                    except ValueError:
                                        print("Invalid input. Please enter a number.")

                            else:
                                while True:
                                    new_value = input(f"Enter updated {fields[i]}: ").strip()
                                    if new_value:
                                        break
                                    print(f"{fields[i]} cannot be empty. Please enter a valid value.")

                            updated_values[i] = new_value  # Update the value

                    new_date, new_store, new_details, new_amount, new_category, new_payment = updated_values
                    new_amount = float(str(new_amount).replace('$', '').replace(',', ''))

                    if isinstance(new_category, int):
                        pass 
                    else:
                        new_category = select_category(new_category)

                    if isinstance(new_payment, int):
                        pass
                    else:
                        new_payment = select_payment_method(new_payment)

                    update_expenses(expense_id, new_date, new_store, new_details, new_amount, new_category, new_payment)
                    print("Expense updated successfully.")
                    input("Press Enter to continue.")

                elif choice == "2":
                    print()
                    print("Delete Expense")
                    print("Expenses:")
                    headers = ["No.", "Date", "Store", "Details", "Amount", "Category", "Payment Method"]
                    print(tabulate(formatted_result, headers=headers, tablefmt="grid"))

                    while True:
                        try:
                            expenses_id = int(input("Enter expense number (or 0 to cancel): "))
                            
                            # Prevents deletion if the user enters 0 or an invalid number
                            if expenses_id == 0:
                                print("Deletion canceled.")
                                break

                            if expenses_id < 1 or expenses_id > len(view_expenses()):
                                print("Invalid expense number. Please try again.")
                                continue  # Ask again

                            # Proceed with deletion if valid
                            expense_id = view_expenses()[expenses_id - 1][0]
                            delete_expense(expense_id)
                            print("Expense deleted successfully.")
                            break

                        except ValueError:
                            print("Invalid input. Please enter a number.")

                    press = input("Press Enter to continue.")

                elif choice == "3":
                    pass

        elif choice == "2": # Record Expenses
            print()
            print("Record Expenses")

            if len(view_expenses_category()) == 0:
                print("No expense categories available. Please add an expense category first.")
                input("Press Enter to continue.")
            else:
                # Validate date input
                while True:
                    expense_date = input("Enter date (YYYY-MM-DD): ").strip()
                    try:
                        datetime.datetime.strptime(expense_date, "%Y-%m-%d")  # Check valid date format
                        break
                    except ValueError:
                        print("Invalid date format. Please enter a valid date in YYYY-MM-DD format.")

                # Validate store input
                while True:
                    store = input("Enter store name: ").strip()
                    if store:
                        break
                    print("Store name cannot be empty. Please enter a valid store name.")

                # Validate details input
                while True:
                    details = input("Enter details: ").strip()
                    if details:
                        break
                    print("Details cannot be empty. Please enter valid details.")

                # Validate amount input
                while True:
                    try:
                        amount = float(input("Enter amount (must be a positive number): "))
                        if amount > 0:
                            break
                        print("Amount must be a positive number.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                # Display expense categories
                print("\nExpense Categories:")
                category_list = view_expenses_category()
                for row in category_list:
                    print(f"{row[0]} - {row[1]}")

                # Validate category ID input
                valid_category_ids = [row[0] for row in category_list]  # Get valid category IDs
                while True:
                    try:
                        category_id = int(input("Enter category ID: "))
                        if category_id in valid_category_ids:
                            break
                        print("Invalid category ID. Please enter a valid ID from the list.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                # Display payment methods
                print("\nPayment Methods:")
                payment_list = view_payment_method()
                for row in payment_list:
                    print(f"{row[0]} - {row[1]}")

                # Validate payment method ID input
                valid_payment_ids = [row[0] for row in payment_list]  # Get valid payment method IDs
                while True:
                    try:
                        payment_method_id = int(input("Enter payment method ID: "))
                        if payment_method_id in valid_payment_ids:
                            break
                        print("Invalid payment method ID. Please enter a valid ID from the list.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                # If all inputs are valid, add the expense
                add_expense(expense_date, store, details, amount, category_id, payment_method_id)
                print("Expense added successfully.")
                input("Press Enter to continue.")

        elif choice == "3": # View Total Expenses per Category
            print()
            print("Total Expenses per Category:")
            if len(total_expenses_per_category()) == 0:
                print("No expenses available.")
                press = input("Press Enter to continue.")
            else:
                headers = ["Category", "Total Expenses"]
                print(tabulate(total_expenses_per_category(), headers=headers, tablefmt="grid"))
                press = input("Press Enter to continue.")
                
        elif choice == "4": # Set Income Budget
            print()
            print("Set Income Budget")

            while True:
                source = input("Enter income source (or 0 to cancel): ").strip()
                if source == "0":
                    print("Income budget setting canceled. Returning to the main menu...")
                    break  # Go back to the main menu
                if source:
                    while True:
                        try:
                            amount = float(input("Enter amount (or 0 to cancel): "))
                            if amount == 0:
                                print("Income budget setting canceled. Returning to the main menu...")
                                break  # Go back to the main menu
                            if amount > 0:
                                add_income(source, amount, month.strftime("%B"))
                                print("Income added successfully.")
                                input("Press Enter to continue.")
                                break  # Exit amount input loop
                            print("Amount must be a positive number.")
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                    break  # Exit source input loop

            # Continue to the main menu instead of exiting
            continue

        elif choice == "5": # Add Expense Category
            print()
            print("Add Expense Category")

            # Ensure category name is not blank
            while True:
                category_name = input("Enter expense category name: ").strip()
                if category_name:
                    break
                print("Expense category name cannot be empty. Please enter a valid name.")

            add_expense_category(category_name)
            input("Press Enter to continue.")

        elif choice == "6": # View Expenses Category
            categories = view_expenses_category()
            print("\nExpense Categories:")
            if not categories:
                print("No expense categories available.")
                input("Press Enter to continue.")
            else:
                headers = ["No.", "Category"]
                print(tabulate(categories, headers=headers, tablefmt="grid"))

                print("\nSelect Option:")
                print("[1] Edit Expense Category")
                print("[2] Delete Expense Category")
                print("[3] Back to Main Menu")

                while True:
                    option = input("Choose an option (1-3): ").strip()
                    if option in ["1", "2", "3"]:
                        break
                    print("Invalid option. Please enter 1, 2, or 3.")

                if option == "1":  # Edit Category
                    print("\nEdit Expense Category")
                    print(tabulate(categories, headers=headers, tablefmt="grid"))

                    while True:
                        try:
                            category_id = int(input("Enter category ID: "))
                            if any(cat[0] == category_id for cat in categories):
                                break
                            print("Invalid category ID. Please enter a valid ID from the list.")
                        except ValueError:
                            print("Invalid input. Please enter a numeric category ID.")

                    while True:
                        new_category_name = input("Enter new category name: ").strip()
                        if new_category_name:
                            break
                        print("Category name cannot be empty. Please enter a valid name.")

                    update_category_name(category_id, new_category_name)
                    print(f"Category updated to '{new_category_name}' successfully.")
                    input("Press Enter to continue.")

                elif option == "2":  # Delete Category
                    print("\nDelete Expense Category")
                    print(tabulate(categories, headers=headers, tablefmt="grid"))

                    while True:
                        try:
                            category_id = int(input("Enter category ID to delete: "))
                            if any(cat[0] == category_id for cat in categories):
                                break
                            print("Invalid category ID. Please enter a valid ID from the list.")
                        except ValueError:
                            print("Invalid input. Please enter a numeric category ID.")

                    confirm = input(f"Are you sure you want to delete category ID {category_id}? (Y/N): ").strip().lower()
                    if confirm == "y":
                        delete_category(category_id)
                        print("Category deleted successfully.")
                    else:
                        print("Deletion canceled.")

                    input("Press Enter to continue.")

                elif option == "3":  # Back to Main Menu
                    pass

        elif choice == "7": # Exit
            print("Exiting program. Goodbye!")
            break

        else: # Invalid option
            print("Invalid option. Try again.")

if __name__ == "__main__":
    menu()
