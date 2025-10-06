import pandas as pd
import os

def create_file(file_path):
    if not os.path.exists(file_path) or (os.path.exists(file_path) and os.path.getsize(file_path) == 0): # Checking if the file exists
        df = pd.DataFrame(columns=["ID", "Date", "Type", "Category", "Amount", "Note"]) #Creating a dataframe head row, in case the file doesnt exist
        df.to_csv(file_path, index=False) # Exporting dataframe to csv file
        return df
    else:
        df = load_data(file_path)
        return df

def load_data(file_path):
    if not os.path.exists(file_path):
        create_file(file_path)
    df = pd.read_csv(file_path)

    # Ensure expected columns exist
    for col in ["ID","Date","Type","Category","Amount","Note"]:
        if col not in df.columns:
            df[col] = pd.Series(dtype="object")  # temporary

    # Coerce types safely
    # For ID: nullable integer (handles empty DF)
    if "ID" in df.columns:
        try:
            df["ID"] = df["ID"].astype("Int64")
        except Exception:
            # If conversion fails, fill with NaN Int64 and no crash
            df["ID"] = pd.Series([pd.NA]*len(df), dtype="Int64")

    # Amount: try numeric, leave NaN if impossible
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    df["Note"] = df["Note"].fillna("")  # replaces any NaN with empty string
    
    return df

def save_data(file_path, df):
    df.to_csv(file_path, index=False)


def add_record(file_path, record):
    if not os.path.exists(file_path): #In case the user tries to add a record, without having the file created
        create_file(file_path)
    df = load_data(file_path)
    
    if "ID" not in record:
        if df.empty or df["ID"].isna().all():
            new_id = 1
        else:
            new_id = int(df["ID"].max()) + 1
        record["ID"] = new_id
    
    # Build row DF and align columns
    row_df = pd.DataFrame([record])
    row_df = row_df.reindex(columns=df.columns)  # missing columns get NaN
    df = pd.concat([df, row_df], ignore_index=True)
    save_data(file_path, df)
    return df