# To Perform operational feature engineering
# and KPI preparation for inventory analysis.

# Data Loading
import pandas as pd

df = pd.read_csv("data/processed/final_dataset.csv")

# Fix Negatives in Inventory
df['inventory_qty'] = df['inventory_qty'].clip(lower=0)

# check nulls
df.isnull().sum()

# Feature Engineering
df['date'] = pd.to_datetime(
    df['date'],
    format='mixed',
    dayfirst=True
)
df['day_of_week'] = df['date'].dt.day_name()
df['month'] = df['date'].dt.month
df['weekend'] = df['date'].dt.weekday >= 5

# DEMAND-INVENTORY GAP
df['gap'] = df['demand_qty'] - df['inventory_qty']

# Fill rate
df['fill_rate'] = df['fulfilled_qty'] / df['demand_qty']

# STOCKOUT VALIDATION
df['calc_stockout'] = (df['demand_qty'] > df['inventory_qty']).astype(int)

# AGGREGATED DATA (FOR ANALYSIS)

# Product-level
product_summary = df.groupby('product_name').agg({
    'demand_qty': 'sum',
    'stockout_flag': 'sum',
    'fill_rate': 'mean'
}).reset_index()

# SAVE CLEAN DATA
df.to_csv("data/processed/cleaned_dataset.csv", index=False)

print(df.head(20))
