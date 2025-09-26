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
        load_data(self.data_file)
        if len(self.df) == 0: # Verifies if the dataframe as any information on it
            return "There were no records added."
        return tabulate(self.df, headers='keys', tablefmt='fancy_grid', showindex=False)

        
    def calculate_total_expense(self):
        if len(self.df) == 0:
            return "There were no expenses added."
        total_expenses_df = self.df[self.df['Type'] == 'Expense']
        return total_expenses_df['Amount'].sum()
            
                

    # def calculate_expenses_category(self):

    # def calculate_monthly_budget(self):

    # def calculate_min_expense(self):

    # def calculate_max_expense(self):

    # def calculate_avg_expenses(self):

    # def print_monthly_report(self)
        

file = "data/budget_data.csv"
budget = BudgetTracker(file)
print(budget.calculate_total_expense())

