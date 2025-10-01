from budget.file_handling import create_file, load_data, save_data, add_record
from tabulate import tabulate
from datetime import datetime

class BudgetTracker:
    def __init__(self, data_file):
        self.data_file = data_file
        self.df = load_data(data_file)

    def add_expense(self, date, category, amount, note=""):
        # Prepare parameters for validation
        params = {
            "date": date,
            "category": category,
            "amount": amount,
            "note": note
        }

        validated = self.validate_record(**params)
        if isinstance(validated, str):  # validation error returned
            return validated
        
        if self.df.empty:
            new_id = 1
        else:
            new_id = self.df['ID'].max() + 1
            
        record = {
            "ID": new_id,
            "Date": validated["Date"],
            "Type": "Expense", # Default value of type in add_expense function
            "Category": validated["Category"], 
            "Amount": validated["Amount"],
            "Note": validated["Note"]
            }
        add_record(self.data_file, record)
        self.df = load_data(self.data_file) # Refresh the file and the value stored in the variable

    def add_income(self, date, category, amount, note=""):
        # Prepare parameters for validation
        params = {
            "date": date,
            "category": category,
            "amount": amount,
            "note": note
        }

        validated = self.validate_record(**params)
        if isinstance(validated, str):  # validation error returned
            return validated
        
        if self.df.empty:
            new_id = 1
        else:
            new_id = self.df['ID'].max() + 1

        record = {
            "ID": new_id,
            "Date": validated["Date"],
            "Type": "Income", # Default value of type in add_income function
            "Category": validated["Category"], 
            "Amount": validated["Amount"],
            "Note": validated["Note"]
        }
        add_record(self.data_file, record) # Calling add_record to add the information to the df and export it to csv 
        self.df = load_data(self.data_file)

    def view_all_records(self):
        return self.df

        
    def calculate_total_expense(self):
        total_expenses_df = self.df[self.df['Type'] == 'Expense'] # Get all the rows with Expense Type
        return total_expenses_df['Amount'].sum()
    
    def calculate_total_income(self):
        total_income_df = self.df[self.df['Type'] == 'Income']
        return total_income_df['Amount'].sum()
                

    def calculate_expenses_category(self):
        expenses = self.df[self.df['Type'] == 'Expense']
        category = expenses.groupby('Category')['Amount'].sum() # Group by Category and gets total sum of each
        category_df = category.reset_index(name="Total") # Convert the grouped Series to a DataFrame and name the summed column 'Total'
        return category_df
        
    def calculate_income_category(self):
        incomes = self.df[self.df['Type'] == 'Income']
        category_df = incomes.groupby('Category')['Amount'].sum()
        category_df = category_df.reset_index(name="Total")
        return category_df

    def calculate_monthly_budget(self):
        pass # Could be implemented later if monthly tracking is needed

    def calculate_min_expense(self):
        expenses = self.df[self.df['Type'] == 'Expense']
        return expenses['Amount'].min()
        # min_expense = self.df[self.df['Amount'] == self.df['Amount'].min()].iloc[0]
        # return min_expense[['Category', 'Amount']]  Formatting Output for UX

    def calculate_min_income(self):
        incomes = self.df[self.df['Type'] == 'Income']
        return incomes['Amount'].min()

    def calculate_max_expense(self):
        expenses = self.df[self.df['Type'] == 'Expense']
        return expenses['Amount'].max()
    
    def calculate_max_income(self):
        incomes = self.df[self.df['Type'] == 'Income']
        return incomes['Amount'].max()

    def calculate_avg_expenses(self):
        expenses = self.df[self.df['Type'] == 'Expense']
        return expenses['Amount'].mean()
    
    def calculate_avg_income(self):
        incomes = self.df[self.df['Type'] == 'Income']
        return incomes['Amount'].mean()

    def print_monthly_report(self):
        pass # Could be implemented later if monthly tracking is needed

    def print_report(self):
        max_value = self.calculate_max_expense() # Get the maximum expense value
        category = self.df[self.df['Amount'] == max_value]['Category'] # Find categories corresponding to the max expense
        categories_str = ", ".join(category.tolist()) # Convert categories to a string, allowing multiple categories if needed
        print("===== Budget Report =====\n")
        print(f"Total Income: {self.calculate_total_income()}€\n")
        print(f"Total Expenses: {self.calculate_total_expense()}€\n")
        print(f"Most Expensive Purchase: {max_value}€ ({categories_str})\n")
        print(f"Average Expense: {self.calculate_avg_expenses()}€\n")
        print(f"Highest Income: {self.calculate_max_income()}€\n")
        print(f"Average Income: {self.calculate_avg_income()}€\n")
        print(f"Expenses by category:\n {self.calculate_expenses_category()}\n")

    def delete_one_row(self, delete_id):
        if delete_id not in self.df['ID'].values:
            raise ValueError(f"Record with ID {delete_id} not found!")
        self.df = self.df[self.df['ID'] != delete_id] #keeps all rows where ID != id
        save_data(self.data_file, self.df)
    
    def delete_all_rows(self):
        self.df = self.df.iloc[0:0]
        save_data(self.data_file,self.df)

    def update_record(self, record_id, field, new_value):
        if record_id not in self.df['ID'].values:
            raise ValueError(f'Record with ID {record_id} not found!')

        # Prepare parameters for validation
        params = {key: None for key in ["date", "category", "amount", "note"]}
        params[field.lower()] = new_value

        validated = self.validate_record(**params)
        if isinstance(validated, str):  # validation error returned
            return validated

        # Assign only the validated value for the field
        self.df.loc[self.df['ID'] == record_id, field] = validated[field.lower()]
        save_data(self.data_file, self.df)
    
    def validate_record(self, date=None, category=None, amount=None, note=None):
        validated = {}

        if date is not None:
            try:
                datetime.strptime(date, '%d/%m/%y')
            except ValueError:
                return "Invalid date format. Use DD/MM/YY"
            if not date:
                return "Date cannot be empty!"
            validated["Date"] = date

        if category is not None:
            if not isinstance(category, str):
                return "Category must be a string"
            if not category:
                return "Category cannot be empty!"
            validated["Category"] = category

        if amount is not None:
            try:
                amount = float(amount)
            except ValueError:
                return "Amount must be a number"
            if not amount:
                return "Amount cannot be empty!"
            if str(amount).strip() == "":
                return "Amount cannot be negative"
            validated["Amount"] = amount

        if note is not None:
            if not isinstance(note, str):
                return "Note must be a string"
            validated["Note"] = note

        return validated
    
    def update_type(self, row_id):
        if row_id not in self.df['ID'].values:
            raise ValueError(f'Record with ID {row_id} not found!')
        current_type = self.df.loc[self.df['ID'] == row_id, 'Type'].iloc[0] 
        if current_type == "Expense":
            self.df.loc[self.df['ID'] == row_id, 'Type'] = "Income"
        else:
            self.df.loc[self.df['ID'] == row_id, 'Type'] = "Expense"
        save_data(self.data_file, self.df)           