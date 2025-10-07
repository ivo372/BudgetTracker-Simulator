import pytest
import pandas as pd
import pandas.testing as pdt
from budget.core_functions import BudgetTracker
from budget.file_handling import create_file, load_data

# -------------------------------
# Fixture: prepares fresh budget instance per test
# -------------------------------
@pytest.fixture
def budget_instance(tmp_path):
    file = tmp_path / "budget.csv"
    create_file(file)
    return BudgetTracker(file), file

# -------------------------------
# Functional tests
# -------------------------------

def test_add_income_add_expense(budget_instance):
    budget, file = budget_instance

    # Test adding records
    budget.add_income("28/09/25", "Salary", 1500.98, "salary")
    budget.add_expense("26/09/25", "Eletronics", 104, "")
    budget.add_income("28/09/25", "Salary", 1500.98, "salary")
    df = load_data(file)
    assert len(df) == 3
    expected_row1 = ["28/09/25", "Income", "Salary", 1500.98, "salary"]
    assert list(df.loc[0][['Date','Type','Category','Amount','Note']]) == expected_row1
    # Default note
    assert df.loc[1]['Note'] == ""

def test_calculate_total_expense_calculate_total_income(budget_instance):
    budget, file = budget_instance
    # No records
    assert budget.calculate_total_expense() == 0
    assert budget.calculate_total_income() == 0
    # Add records
    budget.add_expense("26/09/25", "Eletronics", 104, "")
    budget.add_income("28/09/25", "Salary", 1500.98, "salary")
    df = load_data(file)
    assert budget.calculate_total_income() == df.loc[1]['Amount']
    assert budget.calculate_total_expense() == df.loc[0]['Amount']

def test_max_min_avg_expense_and_max_in_avg_income(budget_instance):
    budget, file = budget_instance
    # Empty dataframe
    assert budget.calculate_min_expense() == 0
    assert budget.calculate_max_expense() == 0
    assert budget.calculate_avg_expenses() == 0
    assert budget.calculate_min_income() == 0
    assert budget.calculate_max_income() == 0
    assert budget.calculate_avg_income() == 0
    # Add single records
    budget.add_expense("26/09/25", "Eletronics", 104, "")
    budget.add_income("28/09/25", "Salary", 1500.98, "salary")
    df = load_data(file)
    assert budget.calculate_min_expense() == df.loc[0,'Amount']
    assert budget.calculate_max_income() == df.loc[1,'Amount']
    # Multiple records
    budget.add_expense("26/09/25", "Eletronics", 60, "")
    budget.add_income("28/09/25", "Salary", 100, "salary")
    df = load_data(file)
    assert budget.calculate_min_expense() == df[df['Type']=='Expense']['Amount'].min()
    assert budget.calculate_max_income() == df[df['Type']=='Income']['Amount'].max()

def test_expenses_category_and_income_category(budget_instance):
    budget, file = budget_instance
    # Empty
    assert budget.calculate_expenses_category().empty
    assert budget.calculate_income_category().empty
    # Add records
    budget.add_expense("26/09/25", "Eletronics", 104, "")
    budget.add_income("28/09/25", "Salary", 1500.98, "salary")
    expected_expense = pd.DataFrame([{"Category":"Eletronics","Total":104.0}])
    expected_income = pd.DataFrame([{"Category":"Salary","Total":1500.98}])
    pdt.assert_frame_equal(budget.calculate_expenses_category(), expected_expense)
    pdt.assert_frame_equal(budget.calculate_income_category(), expected_income)

def test_delete_one_row(budget_instance):
    budget, _ = budget_instance
    budget.add_expense("01/10/25","Food",50)
    budget.delete_one_row(1)
    assert budget.df.empty
    # Non-existent row
    with pytest.raises(ValueError):
        budget.delete_one_row(99)

def test_delete_all_rows(budget_instance):
    budget, _ = budget_instance
    budget.add_expense("01/10/25","Food",50)
    budget.add_income("02/10/25","Salary",1000)
    budget.delete_all_rows()
    assert budget.df.empty

def test_update_record(budget_instance):
    budget, _ = budget_instance
    budget.add_expense("01/10/25","Food",50)
    budget.update_record(1,"Category","Groceries")
    assert budget.df.loc[0,"Category"]=="Groceries"
    # Invalid updates
    with pytest.raises(ValueError, match="Amount must be positive!"):
        budget.update_record(1, "Amount", -100)
    with pytest.raises(ValueError, match="Invalid date"):
        budget.update_record(1, "Date", "2025-10-01")

def test_update_type(budget_instance):
    budget, _ = budget_instance
    budget.add_expense("01/10/25","Food",50)
    assert budget.df.loc[0,"Type"]=="Expense"
    budget.update_type(1)
    assert budget.df.loc[0,"Type"]=="Income"
    budget.update_type(1)
    assert budget.df.loc[0,"Type"]=="Expense"
    with pytest.raises(ValueError):
        budget.update_type(999)

def test_view_all_records(budget_instance):
    budget, _ = budget_instance
    pdt.assert_frame_equal(budget.view_all_records(), budget.df)
    budget.add_expense("26/09/25","Eletronics",104,"")
    budget.add_income("28/09/25","Salary",1500.98,"salary")
    expected_output = pd.DataFrame([
        {"ID": 1, "Date":"26/09/25","Type":"Expense","Category":"Eletronics","Amount":104.0,"Note":""},
        {"ID": 2, "Date":"28/09/25","Type":"Income","Category":"Salary","Amount":1500.98,"Note":"salary"}
    ])
    # convert ID to nullable Int64
    expected_output["ID"] = expected_output["ID"].astype("Int64")
    
    pdt.assert_frame_equal(budget.view_all_records(), expected_output)

def test_print_report(budget_instance,capsys):
    budget, _ = budget_instance
    budget.print_report()
    captured = capsys.readouterr()
    assert "Total Expenses:" in captured.out
    assert "Most Expensive Purchase:" in captured.out
    budget.add_expense("26/09/25","Electronics",104,"")
    budget.add_income("28/09/25","Salary",1500.98,"salary")
    budget.print_report()
    captured = capsys.readouterr()
    assert "104" in captured.out
    assert "1500.98" in captured.out

# -------------------------------
# Defensive / edge-case tests
# -------------------------------
def test_validate_record_defensive(budget_instance):
    budget, _ = budget_instance
    assert "invalid date" in budget.validate_record(date="2025-10-01").lower()
    assert "cannot be empty" in budget.validate_record(date="").lower()
    assert "must be a non-empty string" in budget.validate_record(category=123).lower()
    assert "must be a non-empty string" in budget.validate_record(category="").lower()
    assert "must be a number" in budget.validate_record(amount="abc").lower()
    assert "must be positive" in budget.validate_record(amount=-50).lower()
    assert "positive" in budget.validate_record(amount=0).lower()
    assert "must be a string" in budget.validate_record(note=123).lower()

def test_empty_dataframe_calculations(budget_instance):
    budget, _ = budget_instance
    assert budget.calculate_total_expense()==0
    assert budget.calculate_total_income()==0
    assert budget.calculate_min_expense()==0
    assert budget.calculate_max_expense()==0
    assert budget.calculate_avg_expenses()==0
    assert budget.calculate_min_income()==0
    assert budget.calculate_max_income()==0
    assert budget.calculate_avg_income()==0
    assert budget.calculate_expenses_category().empty
    assert budget.calculate_income_category().empty

def test_min_max_avg_with_same_values(budget_instance):
    budget, _ = budget_instance
    budget.add_expense("01/10/25","Food",100)
    budget.add_expense("01/10/25","Food",100)
    budget.add_income("02/10/25","Salary",500)
    budget.add_income("02/10/25","Salary",500)
    assert budget.calculate_min_expense()==100
    assert budget.calculate_max_expense()==100
    assert budget.calculate_avg_expenses()==100
    assert budget.calculate_min_income()==500
    assert budget.calculate_max_income()==500
    assert budget.calculate_avg_income()==500
