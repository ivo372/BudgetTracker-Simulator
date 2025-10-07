from budget.core_functions import BudgetTracker
from tabulate import tabulate
import re
import os

def main():
    print("=== Welcome to the Budget Simulator ===")
    print("\nTips:")
    print("\t- Read the menus carefully.")
    print("\t- Pay attention to the guide messages, they'll be helpful, if you are lost.")

    file_name = input("\nEnter your budget file name (without extension, press Enter for default): ").strip()

    # Strip whitespace
    filename = file_name.strip()
    
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', "", filename)
    
    # Remove all trailing extensions like .csv, .json, .txt
    filename = re.sub(r'(\.[^.]+)+$', '', filename)  # removes last dot + whatever follows, including repeated
    
    # Handle empty filename after cleaning
    if not filename:
        filename = "budget"

    filename = filename + ".csv"

    if filename == "budget.csv" and file_name.strip() != "budget" and file_name.strip() != "":
        print("\n ⚠️  Invalid or unsafe file name detected. Using default: budget.csv")

    # Make sure 'data' folder exists
    folder = "data"
    os.makedirs(folder, exist_ok=True)

    # Build full path
    file_path = os.path.join(folder, filename)

    budget = BudgetTracker(file_path)
    print(f"\n✅ Using budget file: {filename}")

    while True:
        print("\nChoose an option:")
        print("\t1- Add to file")
        print("\t2- Calculations")
        print("\t3- Update file")
        print("\t4- Delete from file")
        print("\t5- Display")
        print("\t6- Exit")

        choice = input("\nChoose one of the option above(1/2/3/4/5/6): ")
        if choice in ("1", "2", "3", "4", "5", "6"):
            if choice == "1":
                while True:
                    print("\nChoose an option:")
                    print("\t1- Add expense")
                    print("\t2- Add income")
                    print("\t3- Back")
                    choice_add = input("\nChoose one option from above(1/2/3): ")
                    if choice_add in ("1", "2", "3"):
                        if choice_add == "1":
                            while True:
                                add_expense_date = input("\nSelect the date of this expense, in this format(DD/MM/YY): ")
                                add_expense_category = input("\nWrite the category name of expense: ")
                                add_expense_amount = input("\nWrite the amount of expense, it should be a positive number: ")
                                add_expense_note = input("\nAdd a note to this expense, if you wish you can leave it empty: ")

                                try:
                                    
                                    # Attempt to add expense
                                    budget.add_expense(add_expense_date,add_expense_category,add_expense_amount,add_expense_note)

                                except ValueError as e:
                                    print(f"\n❌ Failed to add expense: {e}. Try again!")
                                    add_expense_exit = input("\nDo you wish to try again(y/n): ").lower().strip()
                                    if add_expense_exit not in ("y", "yes", "yep", "ye"):
                                        break
                                else:
                                    # Get the next ID
                                    add_expense_last_id = budget.df['ID'].max()

                                    # Get the new row
                                    add_expense_new_row = budget.df[budget.df['ID'] == add_expense_last_id]
                                    
                                    print("\n✅ Expense added sucessfully!\n")
                                    print(tabulate(add_expense_new_row, headers='keys', tablefmt='fancy_grid', showindex=False))
                                    break
                        
                        elif choice_add == "2":
                            while True:
                                add_income_date = input("\nSelect the date of this income, in this format(DD/MM/YY): ")
                                add_income_category = input("\nWrite the category name of income: ")
                                add_income_amount = input("\nWrite the amount of income, it should be a positive number: ")
                                add_income_note = input("\nAdd a note to this income, if you wish you can leave it empty: ")
                                
                                try:
                                    budget.add_income(add_income_date,add_income_category,add_income_amount,add_income_note)

                                except ValueError as e:
                                    print(f"\n❌ Failed to add income: {e}. Try again!")
                                    add_income_exit = input("\nDo you wish to try again(y/n): ").lower().strip()
                                    if add_income_exit not in ("y", "yes", "yep", "ye"):
                                        break
                                else:
                                    add_income_last_id = budget.df['ID'].max()
                                    add_income_new_row = budget.df[budget.df['ID'] == add_income_last_id]
                                    print("\n✅ Income added sucessfully!\n")
                                    print(tabulate(add_income_new_row, headers='keys', tablefmt='fancy_grid', showindex=False))
                                    break
                        
                        elif choice_add == "3":
                            break
                        
                    else:
                        print("\n❌ Invalid choice. Select an option between 1 and 3!")
                        continue
            
            elif choice == "2":
                while True:
                    print("\nCalculations:")
                    print("\t1- Calculate total expense/income")
                    print("\t2- Calculate expense/income by category")
                    print("\t3- Calculate expense/income min/max/avg")
                    print("\n4- Back")

                    choice_calculations = input("\nSelect one of the options above(1/2/3/4): ")

                    if choice_calculations == "1":
                        while True:
                            print("\nCalculate Totals:")
                            print("\t1- Calculate total expense")
                            print("\t2- Calculate total income")
                            print("\n3- Back")

                            choice_totals = input("\nSelect one of the options above(1/2/3): ")

                            if choice_totals == "1":
                                total_expense = budget.calculate_total_expense()
                                print(f"\nThe total amount of expenses you have is: {total_expense}€")
                                
                            elif choice_totals == "2":
                                total_income = budget.calculate_total_income()
                                print(f"\nThe total amount of income you have is: {total_income}")
                                
                            elif choice_totals == "3":
                                break

                            else:
                                print("\n❌ Invalid choice. Select a number between 1 and 3")
                                continue
                        
                    elif choice_calculations == "2":
                        while True:
                            print("\nCalculate by category:")
                            print("\t1- Calculate expense by category")
                            print("\t2- Calculate income by category")
                            print("\n3- Back")

                            choice_by_category = input("\nSelect one of the options above(1/2/3): ")

                            if choice_by_category == "1":
                                df_expense_category = budget.calculate_expenses_category()
                                    
                                if df_expense_category.empty:
                                    print("No records of expenses recorded ❌")

                                print(tabulate(df_expense_category, headers='keys', tablefmt='fancy_grid', showindex=False))

                            elif choice_by_category == "2":
                                df_income_category = budget.calculate_income_category()
                                    
                                if df_income_category.empty:
                                    print("No records of income recorded ❌")

                                print(tabulate(df_income_category, headers='keys', tablefmt='fancy_grid', showindex=False))

                            elif choice_by_category == "3":
                                break

                            else:
                                print("\n❌ Invalid choice. Select a number between 1 and 3")
                                continue
                        
                    elif choice_calculations == "3":
                        while True:
                            print("\nCalculate min/max/avg:")
                            print("\t1- Calculate max expense")
                            print("\t2- Calculate min expense")
                            print("\t3- Calculate avg expense")
                            print("\t4- Calculate max income")
                            print("\t5- Calculate min income")
                            print("\t6- Calculate avg income")
                            print("\n7- Back")

                            choices_min_max_avg = input("\nSelect one of the options above(1/2/3/4/5/6/7): ")

                            if choices_min_max_avg == "1":
                                max_expense = budget.calculate_max_expense()
                                print(f"\nThe highest expense in your records is: {max_expense}€")
                                
                            elif choices_min_max_avg == "2":
                                min_expense = budget.calculate_min_expense()
                                print(f"\nThe lowest expense in your records is: {min_expense}€")
                                
                            elif choices_min_max_avg == "3":
                                avg_expense = budget.calculate_avg_expenses()
                                print(f"\nThe average amount of expenses in your records is: {avg_expense}€")
                                
                            elif choices_min_max_avg == "4":
                                max_income = budget.calculate_max_income()
                                print(f"\nThe highest income in your records is: {max_income}€")

                            elif choices_min_max_avg == "5":
                                min_income = budget.calculate_min_income()
                                print(f"\nThe lowest income in your records is: {min_income}€")
                                
                            elif choices_min_max_avg == "6":
                                avg_income = budget.calculate_avg_income()
                                print(f"\nThe average income in your records is: {avg_income}€")
                                
                            elif choices_min_max_avg == "7":
                                break

                            else:
                                print("\n❌ Invalid choice. Select a number between 1 and 7")
                                continue

                    elif choice_calculations == "4":
                        break

                    else:
                        print("\n❌ Invalid choice. Select a number between 1 and 7")
                        continue

            elif choice == "3":
                print("\nRead This:")
                print("\n\tOption 1 requires that you know the ID of the row you want to update,\n you can access that ID by going to 'Display'")
                print("\n\tOption 2 is to exchange the type of record,\n" \
                "meaning Income changes for Expense and Expense changes for Income.\n" \
                "By selecting this option the change will take immediate effect,\n" \
                "so becareful if you don't want to change the type of record")

                while True:
                    print("\nUpdate Options:")
                    print("\t1- Update record section")
                    print("\t2- Update Type")
                    print("\n3- Back")

                    choice_update = input("\nSelect one of the options above(1/2/3): ")  

                    if choice_update == "1":
                        while True:
                            record_id = int(input("Write the 'id' of the record you want to update: "))
                            field = input("Write the 'field' you want to update(Date/Category/Amount/Note): ")
                            new_value = input("Write the new value for the field you want to update: ")

                            try:
                                budget.update_record(record_id, field, new_value)

                            except ValueError as e:
                                print(f"\n❌ Failed to update record: {e}. Try again!")
                                update_record_exit = input("\nDo you wish to try again(y/n): ").lower().strip()
                                if update_record_exit not in ("y", "yes", "yep", "ye"):
                                    break
                            else:
                                update_record_next_id = budget.df['ID'].max()
                                update_record_new_row = budget.df[budget.df['ID'] == update_record_next_id]
                                print("\n✅ Record Field updated sucessfully!\n")
                                print(tabulate(update_record_new_row, headers='keys', tablefmt='fancy_grid', showindex=False))
                                break
                    
                    elif choice_update == "2":
                        while True:
                            row_id = int(input("Write the 'id' of the record you want to update the type: "))

                            try:
                                budget.update_type(row_id)

                            except ValueError as e:
                                print(f"\n❌ Failed to update type: {e}. Try again!")
                                update_type_exit = input("\nDo you wish to try again(y/n): ").lower().strip()
                                if update_type_exit not in ("y", "yes", "yep", "ye"):
                                    break
                            else:
                                update_type_next_id = budget.df['ID'].max()
                                update_type_new_row = budget.df[budget.df['ID'] == update_type_next_id]
                                print("\n✅ Record Type updated sucessfully!\n")
                                print(tabulate(update_type_new_row, headers='keys', tablefmt='fancy_grid', showindex=False))
                                break
                    
                    elif choice_update == "3":
                        break

                    else:
                        print("\n❌ Invalid choice. Select a number between 1 and 3")
                        continue
                
            elif choice == "4":
                print("\nRead This:")
                print("\n\tOption 1 requires the record id you want to delete, to find the id, \n" \
                "you can go to 'display option', and find the id in the first column")
                print("\n\tOption 2 is to delete all records currently present on the file, \n " \
                "by selecting this option all records will be deleted and there is no back up, so be careful")
                
                while True:
                    print("\nChoose an option:")
                    print("\t1- Delete one record")
                    print("\t2- Delete all records")
                    print("\n3- Back")

                    choice_delete = input("\nSelect one of the options above(1/2/3): ")

                    if choice_delete == "1":
                        while True:
                            delete_id = int(input("\nWrite the id of the record you want to delete: "))

                            try:
                                budget.delete_one_row(delete_id)
                            except ValueError as e:
                                print(f"\n❌ Failed to delete record: {e}. Try again!")
                                delete_row_exit = input("\nDo you wish to try again(y/n): ").lower().strip()
                                if delete_row_exit not in ("y", "yes", "yep", "ye"):
                                    break
                            else:
                                print("\n✅ Record deleted sucessfully!")
                                break

                    elif choice_delete == "2": 
                        try:
                            budget.delete_all_rows()
                        except ValueError as e:
                            print(f"\n❌ Failed to delete all records: {e}. Try again!")
                        else:
                            print("\n✅ All record deleted sucessfully!")

                    elif choice_delete == "3":
                        break

                    else:
                        print("\n❌ Invalid choice. Select an option between 1 and 3!")
                        continue
                        
            elif choice == "5":
                while True:
                    print("\nChoose an option:")
                    print("\t1- Display all records")
                    print("\t2- Display all time report")
                    print("\n3- Back")

                    choice_display = input("\nSelect one of the options above(1/2/3): \n")

                    if choice_display == "1":
                        all_records_df = budget.view_all_records()
                        print(tabulate(all_records_df, headers='keys', tablefmt='fancy_grid', showindex=False))
                    
                    elif choice_display == "2":
                        budget.print_report()

                    elif choice_display == "3":
                        break

                    else:
                        print("\n❌ Invalid choice. Select a number between 1 and 3")
                        continue

            elif choice == "6":
                print("✅ Thank you for experimenting our program. Feel free to send any suggetions.")
                break

        else:
            print("\n❌ Invalid choice. Select an option between 1 and 6!")
            continue




    








if __name__ == "__main__":
    main()