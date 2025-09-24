import pandas as pd
from budget.file_handling import create_file, add_record, load_data

def test_create_file(tmp_path):
    # Use tmp_path to create a temporary file
    file = tmp_path / "budget.csv"
    create_file(file)
    # check that the file was created
    assert file.exists()
    #Load the file and check headers
    df = load_data(file)
    expected_columns = ["Date", "Type", "Category", "Amount", "Note"]
    assert list(df.columns) == expected_columns

    # Check that the file is empty(no data yet)
    assert len(df) == 0

def test_add_record(tmp_path):
    #Setup a temporary file
    file = tmp_path / "budget.csv"
    create_file(file)

    record = {
        "Date": "24/09/25",
        "Type": "Expense",
        "Category": "Food",
        "Amount": 10.0,
        "Note": ""
    }
    record2 = {
        "Date": "27/09/25",
        "Type": "Expense",
        "Category": "Food",
        "Amount": 14.95,
        "Note": ""
    }
    record3 = {
        "Date": "29/09/25",
        "Type": "Expense",
        "Category": "",
        "Amount": 1250,
        "Note": "Laptop"
    }

    add_record(file, record)

    df = load_data(file)

    assert len(df) == 1
    assert df.loc[0]["Amount"] == 10.0
    assert df.loc[0]["Note"] == ''
    add_record(file, record2)
    add_record(file, record3)

    df = load_data(file)
    assert len(df) == 3
    assert df.loc[2]["Amount"] == 1250
    assert isinstance(df.loc[0]["Amount"], float)
    assert isinstance(df.loc[0]["Note"], str)


