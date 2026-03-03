"""
analysis.py
-----------
Runs analytical queries on the cleaned dataset and
prints a summary report — mimicking DAX measures.
"""

import pandas as pd


def load_cleaned(path: str = "data/cleaned_data.csv") -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["Order_Date"])


def kpi_summary(df: pd.DataFrame) -> None:
    print("=" * 55)
    print("         OVERALL KPI SUMMARY")
    print("=" * 55)
    print(f"  Total Revenue        : ₹{df['Revenue'].sum():,.2f}")
    print(f"  Total Profit         : ₹{df['Net_Profit'].sum():,.2f}")
    print(f"  Avg Profit Margin    : {df['Profit_Margin'].mean():.2f}%")
    print(f"  Total Orders         : {df['Order_ID'].nunique()}")
    print(f"  Total Units Sold     : {df['Quantity'].sum()}")
    print(f"  Unique Products      : {df['Product'].nunique()}")
    print("=" * 55)


def top_products(df: pd.DataFrame, n: int = 5) -> None:
    print(f"\n--- TOP {n} PRODUCTS BY REVENUE ---")
    result = (
        df.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )
    result["Revenue"] = result["Revenue"].map("₹{:,.2f}".format)
    print(result.to_string(index=False))


def revenue_by_category(df: pd.DataFrame) -> None:
    print("\n--- REVENUE & PROFIT BY CATEGORY ---")
    result = (
        df.groupby("Category")
        .agg(Revenue=("Revenue", "sum"), Profit=("Net_Profit", "sum"))
        .sort_values("Revenue", ascending=False)
        .reset_index()
    )
    result["Revenue"] = result["Revenue"].map("₹{:,.2f}".format)
    result["Profit"]  = result["Profit"].map("₹{:,.2f}".format)
    print(result.to_string(index=False))


def regional_performance(df: pd.DataFrame) -> None:
    print("\n--- REGIONAL PERFORMANCE ---")
    result = (
        df.groupby("Region")
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Net_Profit", "sum"),
            Orders=("Order_ID", "count"),
        )
        .sort_values("Revenue", ascending=False)
        .reset_index()
    )
    result["Revenue"] = result["Revenue"].map("₹{:,.2f}".format)
    result["Profit"]  = result["Profit"].map("₹{:,.2f}".format)
    print(result.to_string(index=False))


def monthly_revenue_trend(df: pd.DataFrame) -> None:
    print("\n--- MONTHLY REVENUE TREND ---")
    result = (
        df.groupby(["Month_Num", "Month"])["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Month_Num")
    )
    for _, row in result.iterrows():
        bar = "█" * int(row["Revenue"] / 200)
        print(f"  {row['Month']:<12}  {bar}  ₹{row['Revenue']:,.2f}")


if __name__ == "__main__":
    df = load_cleaned()
    kpi_summary(df)
    top_products(df)
    revenue_by_category(df)
    regional_performance(df)
    monthly_revenue_trend(df)
