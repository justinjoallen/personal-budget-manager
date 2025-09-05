from db_budget_manager import BudgetManagerDB
 
def main():
    manager = BudgetManagerDB()
 
    while True:
        print("\nBudget Manager")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Totals by Category")
        print("4. Delete Expense")
        print("5. Update Expense")
        print("6. Filter Expenses")
        print("7. Export to CSV")
        print("8. Exit")
 
        choice = input("Choose an option: ")
 
        if choice == '1':
            category = input("Enter category: ")
            try:
                amount = float(input("Enter amount: "))
                note = input("Optional note: ")
                manager.add_expense(category, amount, note)
                print("Expense added.")
            except ValueError:
                print("Invalid input.")
        elif choice == '2':
            expenses = manager.view_expenses()
            if not expenses:
                print("No expenses recorded.")
            else:
                print("\nExpenses:")
                for exp in expenses:
                    print(f"[ID: {exp[0]}] Category: {exp[1]} | Amount: ${exp[2]:.2f} | Note: {exp[3]} | Date: {exp[4]}")
        elif choice == '3':
            totals = manager.total_by_category()
            print("\nTotal by Category:")
            for category, total in totals:
                print(f"{category}: ${total:.2f}")
        elif choice == '4':
            try:
                expense_id = int(input("Enter expense ID to delete: "))
                manager.delete_expense(expense_id)
                print("Expense deleted.")
            except ValueError:
                print("Invalid ID.")
        elif choice == '5':
            try:
                expense_id = int(input("Enter expense ID to update: "))
                expenses = manager.view_expenses()
                current = next((e for e in expenses if e[0] == expense_id), None)
 
                if not current:
                    print("Expense ID not found.")
                    continue
 
                print(f"\nCurrent values:")
                print(f"\category: {current[1]}")
                print(f"Amount: ${current[2]:.2f}")
                print(f"Note:  {current[3]}")  
 
                new_category = input("New category (press Enter to keep current): ")
                new_amount_input = input("New amount (press Enter to keep current): ")
                new_note = input("New note (press Enter ro keep current): ")
 
                category = new_category if new_category else current[1]
                amount = float(new_amount_input) if new_amount_input else current [2]
                note = new_note if new_note else current [3]
 
                manager.update_expense(expense_id, category, amount, note)
                print("Expense updated.")
            except ValueError:
                print("Invalid input.")
        elif choice == '6':
            category = input("Filter by category (leave blank to skip): ")
            start_date = input("Start date (YYYY-MM-DD, leave blank to skip): ")
            end_date = input("End date (YYYY-MM-DD, leave blank to skip): ")
            filtered = manager.filter_expenses(
                category if category else None,
                start_date if start_date else None,
                end_date if end_date else None
            )
            if not filtered:
                print("No matching expenses.")
            else:
                print("\nFiltered Expenses:")
                for exp in filtered:
                    print(f"{exp[0]}. {exp[1]} - ${exp[2]:.2f} ({exp[3]}) on {exp[4]}")
        elif choice == '7':
            manager.export_to_csv()
            print("Expenses exported to expenses.csv.")
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
 
if __name__ == "__main__":
    main()