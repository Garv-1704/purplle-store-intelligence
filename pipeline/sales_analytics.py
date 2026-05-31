import pandas as pd

df = pd.read_csv(
    "sales_data/Brigade_Bangalore_10_April_26 (1)bc6219c.csv"
)

revenue = df["total_amount"].sum()
transactions = df["invoice_number"].nunique()
units_sold = df["qty"].sum()
abv = revenue / transactions

print(f"Revenue: ₹{revenue:.2f}")
print(f"Transactions: {transactions}")
print(f"Units Sold: {units_sold}")
print(f"Average Bill Value: ₹{abv:.2f}")

print("\nTop 5 Brands")
print(
    df.groupby("brand_name")["total_amount"]
      .sum()
      .sort_values(ascending=False)
      .head(5)
)

print("\nTop 5 Categories")
print(
    df.groupby("dep_name")["total_amount"]
      .sum()
      .sort_values(ascending=False)
      .head(5)
)