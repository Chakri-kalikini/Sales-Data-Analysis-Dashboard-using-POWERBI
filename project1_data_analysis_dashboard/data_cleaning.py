"""
data_cleaning.py
----------------
Loads raw sales data, cleans and transforms it,
then saves a cleaned version ready for analysis.
"""

import pandas as pd
import os

RAW_PATH   = "data/sales_data.csv"
CLEAN_PATH = "data/cleaned_data.csv"


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"[INFO] Loaded {len(df)} rows from '{path}'")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    print("\n[STEP 1] Checking for nulls...")
    null_counts = df.isnull().sum()
    print(null_counts[null_counts > 0] if null_counts.any() else "  No null values found.")

    print("\n[STEP 2] Dropping duplicate rows...")
    before = len(df)
    df = df.drop_duplicates()
    print(f"  Removed {before - len(df)} duplicates.")

    print("\n[STEP 3] Parsing dates...")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Month"]      = df["Order_Date"].dt.month_name()
    df["Month_Num"]  = df["Order_Date"].dt.month
    df["Quarter"]    = df["Order_Date"].dt.to_period("Q").astype(str)
    df["Year"]       = df["Order_Date"].dt.year

    print("\n[STEP 4] Computing derived KPIs...")
    df["Revenue"]       = df["Sales"] * df["Quantity"]
    df["Net_Profit"]    = df["Profit"] * df["Quantity"]
    df["Profit_Margin"] = (df["Net_Profit"] / df["Revenue"] * 100).round(2)

    print("\n[STEP 5] Standardising text columns...")
    for col in ["Product", "Category", "Region"]:
        df[col] = df[col].str.strip().str.title()

    print(f"\n[DONE] Cleaned dataset shape: {df.shape}")
    return df


def save_data(df: pd.DataFrame, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"[INFO] Cleaned data saved to '{path}'")


if __name__ == "__main__":
    df = load_data(RAW_PATH)
    df = clean_data(df)
    save_data(df, CLEAN_PATH)
    print("\n--- Preview (first 5 rows) ---")
    print(df.head().to_string())
