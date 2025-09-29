import pandas as pd
import pandas.testing as pdt
from budget.core_functions import BudgetTracker
from budget.file_handling import create_file, load_data, add_record

def test_add_income_add_expense(tmp_path):
    # Use tmp_path to create a temporary file
    file = tmp_path / "budget.csv"
    create_file(file)
    
    # Create an instance
    budget = BudgetTracker(file)

    # Load File
    df = load_data(file)

    # Test that the record is actually added to the dataframe.
    budget.add_income("28/09/25", "Salary", 1500.98, "salary")
    df = load_data(file)
    assert len(df) == 1

    # Test multiple additions in sequence.
    budget.add_expense("26/09/25", "Eletronics", 104, "")
    budget.add_income("28/09/25", "Salary", 1500.98, "salary")
    df = load_data(file)
    assert len(df) == 3

    # Verify that the Type column are correctly set.
    expected_row1 = ["28/09/25", "Income", "Salary", 1500.98, "salary"]
    assert list(df.loc[0][['Date', 'Type','Category', 'Amount', 'Note']]) == expected_row1

    # Check that Note defaults to an empty string if not provided.
    expected_output = ""
    assert df.loc[1]['Note'] == expected_output


def test_calculate_total_expense_calculate_total_income(tmp_path):
    # Use tmp_path to create a temporary file
    file = tmp_path / "budget.csv"
    create_file(file)
    
    # Create an instance
    budget = BudgetTracker(file)

    # Load File
    df = load_data(file)

    # Check totals when there are no records (should return 0)
    assert budget.calculate_total_expense() == 0
    assert budget.calculate_total_income() == 0

    # Check totals when the dataframe has mixed types (expenses + income)
    # Calculate totals when there’s a single record
    budget.add_expense("26/09/25", "Eletronics", 104, "")
    budget.add_income("28/09/25", "Salary", 1500.98, "salary")
    df = load_data(file)
    assert budget.calculate_total_income() == df.loc[1]['Amount']
    assert budget.calculate_total_expense() == df.loc[0]['Amount']

    # Calculate totals when there are multiple records
    budget.add_expense("26/09/25", "Eletronics", 104, "")
    budget.add_income("28/09/25", "Salary", 1500.98, "salary")
    df = load_data(file)
    assert budget.calculate_total_income() == df[df[ 'Type' ] == 'Income']['Amount'].sum()
    assert budget.calculate_total_expense() == df[df[ 'Type' ] == 'Expense']['Amount'].sum()

def test_max_min_avg_expense_and_max_in_avg_income(tmp_path):
    # Use tmp_path to create a temporary file
    file = tmp_path / "budget.csv"
    create_file(file)
    
    # Create an instance
    budget = BudgetTracker(file)

    # Load File
    df = load_data(file)

    # Check min/max/avg when there are no records in the dataframe
    assert budget.calculate_min_expense() == 0
    assert budget.calculate_max_expense() == 0
    assert budget.calculate_avg_expenses() == 0
    assert budget.calculate_min_income() == 0
    assert budget.calculate_max_income() == 0
    assert budget.calculate_avg_income() == 0

    # Check totals when the dataframe has mixed types (expenses + income)
    # Single record: max, min, avg all return that same value.
    budget.add_expense("26/09/25", "Eletronics", 104, "")
    budget.add_income("28/09/25", "Salary", 1500.98, "salary")
    df = load_data(file)

    assert budget.calculate_min_expense() == df.loc[0]['Amount']
    assert budget.calculate_max_expense() == df.loc[0]['Amount']
    assert budget.calculate_avg_expenses() == df.loc[0]['Amount']
    assert budget.calculate_min_income() == df.loc[1]['Amount']
    assert budget.calculate_max_income() == df.loc[1]['Amount']
    assert budget.calculate_avg_income() == df.loc[1]['Amount']

    # Multiple records: verify correct calculation.
    budget.add_expense("26/09/25", "Eletronics", 60, "")
    budget.add_income("28/09/25", "Salary", 100, "salary")
    df = load_data(file)
    
    assert budget.calculate_min_expense() == df[df[ 'Type' ] == 'Expense']['Amount'].min()
    assert budget.calculate_max_expense() == df[df[ 'Type' ] == 'Expense']['Amount'].max()
    assert budget.calculate_avg_expenses() == df[df[ 'Type' ] == 'Expense']['Amount'].mean()
    assert budget.calculate_min_income() == df[df[ 'Type' ] == 'Income']['Amount'].min()
    assert budget.calculate_max_income() == df[df[ 'Type' ] == 'Income']['Amount'].max()
    assert budget.calculate_avg_income() == df[df[ 'Type' ] == 'Income']['Amount'].mean()
    
    
    
    # Multiple records with same min or max: return one value
    budget.add_expense("26/09/25", "Eletronics", 104, "")
    budget.add_income("28/09/25", "Salary", 1500.98, "salary")
    df = load_data(file)

    assert budget.calculate_min_expense() == df[df[ 'Type' ] == 'Expense']['Amount'].min()
    assert budget.calculate_max_expense() == df[df[ 'Type' ] == 'Expense']['Amount'].max()
    assert budget.calculate_min_income() == df[df[ 'Type' ] == 'Income']['Amount'].min()
    assert budget.calculate_max_income() == df[df[ 'Type' ] == 'Income']['Amount'].max()


def test_expenses_category_and_income_category(tmp_path):
    # Use tmp_path to create a temporary file
    file = tmp_path / "budget.csv"
    create_file(file)
    
    # Create an instance
    budget = BudgetTracker(file)

    # Load File
    df = load_data(file)

    # Check result when there are no records
    assert budget.calculate_expenses_category().empty
    assert budget.calculate_income_category().empty

    # Single expense/income: returns one category with correct total.
    budget.add_expense("26/09/25", "Eletronics", 104, "")
    budget.add_income("28/09/25", "Salary", 1500.98, "salary")
    df = load_data(file)
    expected_expense = pd.DataFrame([
        {"Category": "Eletronics", "Total": 104.0}
    ])
    expected_income = pd.DataFrame([
        {"Category": "Salary", "Total": 1500.98}
    ])
    pdt.assert_frame_equal(budget.calculate_expenses_category(), expected_expense)
    pdt.assert_frame_equal(budget.calculate_income_category(), expected_income)

    # Multiple expenses: sum per category is correct.
    budget.add_expense("26/09/25", "Eletronics", 104, "")
    budget.add_income("28/09/25", "Salary", 1500.98, "salary")
    df = load_data(file)
    expected_expense_1 = pd.DataFrame([
        {"Category": "Eletronics", "Total": 104.0*2}
    ])
    expected_income_1 = pd.DataFrame([
        {"Category": "Salary", "Total": 1500.98*2}
    ])

    pdt.assert_frame_equal(budget.calculate_expenses_category(), expected_expense_1)
    pdt.assert_frame_equal(budget.calculate_income_category(), expected_income_1)


def test_view_all_records(tmp_path):
    # Use tmp_path to create a temporary file
    file = tmp_path / "budget.csv"
    create_file(file)
    
    # Create an instance
    budget = BudgetTracker(file)

    # Load File
    df = load_data(file)

    # Check for when there are no records
    pdt.assert_frame_equal(budget.view_all_records(), df)

    # Check that the dataframe returned matches what's expected after adding some records.
    budget.add_expense("26/09/25", "Eletronics", 104, "")
    budget.add_income("28/09/25", "Salary", 1500.98, "salary")
    df = load_data(file)

    expected_output = pd.DataFrame([
        {"Date": "26/09/25","Type":"Expense", "Category": "Eletronics", "Amount": 104.0, "Note":""},
        {"Date": "28/09/25","Type":"Income", "Category": "Salary", "Amount": 1500.98, "Note":"salary"}
    ])

    pdt.assert_frame_equal(budget.view_all_records(), expected_output)

def test_print_report(tmp_path, capsys):
    # Use tmp_path to create a temporary file
    file = tmp_path / "budget.csv"
    create_file(file)
    
    # Create an instance
    budget = BudgetTracker(file)

    
    budget.print_report()
    captured = capsys.readouterr()
    assert "Total Expenses:" in captured.out
    assert "Most Expensive Purchase:" in captured.out

    budget.add_expense("26/09/25", "Electronics", 104, "")
    budget.add_income("28/09/25", "Salary", 1500.98, "salary")

    budget.print_report()

    captured_1 = capsys.readouterr()
    assert "104" in captured_1.out     
    assert "1500.98" in captured_1.out
