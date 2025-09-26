import pandas as pd
from budget.core_functions import BudgetTracker
from budget.file_handling import create_file, load_data, add_record

def test_add_expense_add_income_view_all_records_and_calculate_total_expenses(tmp_path):
    # Use tmp_path to create a temporary file
    file = tmp_path / "budget.csv"
    create_file(file)
    
    # Create an instance
    budget = BudgetTracker(file)

    # Test view and calculate with empty file
    df = load_data(file)
    expected_empty_total = "There were no expenses added."
    expected_empty_view = "There were no records added."
    assert budget.view_all_records() == expected_empty_view
    assert budget.calculate_total_expense() == expected_empty_total

    #Test calculate with only incomes
    income3 = budget.add_income("28/09/25", "Salary", 1500.98, "salary")
    income4 = budget.add_income("28/09/25", "Salary", 980, "salary")

    df = load_data(file)
    assert  budget.calculate_total_expense() == 0

    #Call method
    expense1 = budget.add_expense("26/09/25", "Eletronics", 104, "")
    income1 = budget.add_income("28/09/25", "Salary", 1500.98, "salary")
    expense2 = budget.add_expense("26/09/25", "Eletronics", 1250.96, "")
    income2 = budget.add_income("28/09/25", "Salary", 980, "salary")

    #Load the file
    df = load_data(file)

    # test View and calculate(with incomes and expenses) after records were added
    expected_df = pd.DataFrame([
        {"Date":"28/09/25", "Type": "Income", "Category": "Salary", "Amount": 1500.98, "Note": "salary"},
        {"Date":"28/09/25", "Type": "Income", "Category": "Salary", "Amount": 980, "Note": "salary"},
        {"Date":"26/09/25", "Type": "Expense", "Category": "Eletronics", "Amount": 104, "Note": ""},
        {"Date":"28/09/25", "Type": "Income", "Category": "Salary", "Amount": 1500.98, "Note": "salary"},
        {"Date":"26/09/25", "Type": "Expense", "Category": "Eletronics", "Amount": 1250.96, "Note": ""},
        {"Date":"28/09/25", "Type": "Income", "Category": "Salary", "Amount": 980, "Note": "salary"}
    ])
    df = load_data(file)

    amount1 = df.iloc[2]['Amount']
    amount2 = df.iloc[4]['Amount']
    expected_total = amount1 + amount2

    assert budget.df.equals(expected_df)
    assert  budget.calculate_total_expense() == expected_total

    # Check that the row was added and its contents
    # assert len(df) == 2  -- worked
    # expected_row1 = ["26/09/25", "Expense", "Eletronics", 104, ""]
    # assert list(df.loc[0][['Date', 'Type','Category', 'Amount', 'Note']]) == expected_row1 --worked
    # expected_row2 = ["28/09/25", "Income", "Salary", 1500.98, "salary"]
    # assert list(df.loc[1][['Date', 'Type','Category', 'Amount', 'Note']]) == expected_row2 --worked



