import pandas as pd
import os
from tabulate import tabulate

def create_file(file_path):
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Note"])
        df.to_csv(file_path, index=False)
        return tabulate(df, headers='keys', tablefmt='pretty', showindex=False)

def load_data(file_path):
    if not os.path.exists(file_path):
        create_file(file_path)
    df = pd.read_csv(file_path)
    return df

def save_data(file_path, df):
    df.to_csv(file_path, index=False)


def add_record(file_path, record):
    df = load_data(file_path)
    df = pd.concat([df, pd.DataFrame([record])], ignore_index = True)
    save_data(file_path, df)


file = "test.csv"

loaded_test = load_data(file)

record = {"Date": "23/09/25", "Type": "Expense", "Category": "Eletronics", "Amount": 200, "Note": "test"}

record_test = add_record(file, record)
