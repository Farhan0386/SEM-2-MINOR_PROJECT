# Step 1: Import libraries
import pandas as pd
import os

# Step 2: Define file path (update this to your actual file)
file_path = r"C:\Users\farha\GitHub\SEM-2-MINOR_PROJECT\DATA CLEANING OF DATASET\Library.xlsx"

# Step 3: Check if file exists
if not os.path.exists(file_path):
    print("File not found at:", file_path)
else:
    print("File found:", file_path)

    # Step 4: Load file (auto-detect CSV vs Excel)
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        df = pd.read_excel(file_path, engine="openpyxl")  # explicitly use openpyxl
    else:
        raise ValueError("Unsupported file format. Use CSV or Excel.")

    # Step 5: Show dataset info
    print("\n--- Dataset Info ---")
    print(df.info())
    print("\n--- First 5 Rows ---")
    print(df.head())

    # Step 6: Check missing values
    print("\n--- Missing Values ---")
    print(df.isnull().sum())

    # Step 7: Check duplicates
    print("\n--- Duplicate Rows ---")
    print(df.duplicated().sum())

    # Step 8: Clean data
    df = df.drop_duplicates()          # remove duplicates
    df = df.fillna("Unknown")          # fill missing values with placeholder

    # Step 9: Verify cleaning
    print("\n--- After Cleaning ---")
    print("Missing values:", df.isnull().sum().sum())
    print("Duplicate rows:", df.duplicated().sum())

    # Step 10: Save cleaned dataset
    cleaned_path = file_path.replace(".xlsx", "_cleaned.xlsx").replace(".csv", "_cleaned.csv")
    if cleaned_path.endswith(".csv"):
        df.to_csv(cleaned_path, index=False)
    else:
        df.to_excel(cleaned_path, index=False, engine="openpyxl")

    print("Cleaned file saved as:", cleaned_path)
