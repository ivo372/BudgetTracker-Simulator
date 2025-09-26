import pandas as pd
import os
from tabulate import tabulate

def create_file(file_path):
    if not os.path.exists(file_path) or (os.path.exists(file_path) and os.path.getsize(file_path) == 0): # Checking if the file exists
        df = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Note"]) #Creating a dataframe head row, in case the file doesnt exist
        df.to_csv(file_path, index=False) # Exporting dataframe to csv file
        return tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False) # Making the presentation of dataframe looking better in the terminal, so the user sees the result in the terminal
    else:
        df = load_data(file_path)
        return f"The file is already created and contains information! \n{tabulate(df, headers='keys', tablefmt='pretty', showindex=False)}"

def load_data(file_path):
    if not os.path.exists(file_path):
        create_file(file_path)
    df = pd.read_csv(file_path, dtype={"Date": str, "Type": str, "Category": str, "Amount": float, "Note": str}) # reading the csv file for dataframe format
    df["Note"] = df["Note"].fillna('')  # replaces any NaN with empty string
    return df

def save_data(file_path, df):
    df.to_csv(file_path, index=False)


def add_record(file_path, record):
    if not os.path.exists(file_path): #In case the user tries to add a record, without having the file created
        create_file(file_path)
    df = load_data(file_path)
    df = pd.concat([df, pd.DataFrame([record])], ignore_index = True) # Adding one row to the dataframe
    save_data(file_path, df)
    return tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False)
