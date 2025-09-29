from budget.file_handling import create_file, load_data, save_data, add_record
from tabulate import tabulate

class BudgetTracker:
    def __init__(self, data_file):
        self.data_file = data_file
        self.df = load_data(data_file)

    def add_expense(self, date, category, amount, note=""):
        record = {
            "Date": date,
            "Type": "Expense", # Default value of type in add_expense function
            "Category": category, 
            "Amount": amount,
            "Note": note
            }
        add_record(self.data_file, record)
        self.df = load_data(self.data_file) # Refresh the file and the value stored in the variable

    def add_income(self, date, category, amount, note=""):
        record = {
            "Date": date,
            "Type": "Income", # Default value of type in add_income function
            "Category": category, 
            "Amount": amount,
            "Note": note
            }
        add_record(self.data_file, record) # Calling add_record to add the information to the df and export it to csv 
        self.df = load_data(self.data_file)

    def view_all_records(self):
        return self.df

        
    def calculate_total_expense(self):
        if self.df.empty: # Checks for records in the dataframe
            return 0
        total_expenses_df = self.df[self.df['Type'] == 'Expense'] # Get all the rows with Expense Type
        return total_expenses_df['Amount'].sum()
    
    def calculate_total_income(self):
        if self.df.empty:
            return 0
        total_income_df = self.df[self.df['Type'] == 'Income']
        return total_income_df['Amount'].sum()
                

    def calculate_expenses_category(self):
        if self.df.empty:
            return self.df
        expenses = self.df[self.df['Type'] == 'Expense']
        category = expenses.groupby('Category')['Amount'].sum() # Group by Category and gets total sum of each
        category_df = category.reset_index(name="Total") # Convert the grouped Series to a DataFrame and name the summed column 'Total'
        return category_df
        
    def calculate_income_category(self):
        if self.df.empty:
            return self.df
        incomes = self.df[self.df['Type'] == 'Income']
        category_df = incomes.groupby('Category')['Amount'].sum()
        category_df = category_df.reset_index(name="Total")
        return category_df

    def calculate_monthly_budget(self):
        pass # Could be implemented later if monthly tracking is needed

    def calculate_min_expense(self):
        if self.df.empty:
            return 0
        expenses = self.df[self.df['Type'] == 'Expense']
        return expenses['Amount'].min()
        # min_expense = self.df[self.df['Amount'] == self.df['Amount'].min()].iloc[0]
        # return min_expense[['Category', 'Amount']]  Formatting Output for UX

    def calculate_min_income(self):
        if self.df.empty:
            return 0
        incomes = self.df[self.df['Type'] == 'Income']
        return incomes['Amount'].min()

    def calculate_max_expense(self):
        if self.df.empty:
            return 0
        expenses = self.df[self.df['Type'] == 'Expense']
        return expenses['Amount'].max()
    
    def calculate_max_income(self):
        if self.df.empty:
            return 0
        incomes = self.df[self.df['Type'] == 'Income']
        return incomes['Amount'].max()

    def calculate_avg_expenses(self):
        if self.df.empty:
            return 0
        expenses = self.df[self.df['Type'] == 'Expense']
        return expenses['Amount'].mean()
    
    def calculate_avg_income(self):
        if self.df.empty: 
            return 0
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




