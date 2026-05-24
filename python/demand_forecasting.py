"""
Generate rolling demand forecasts and
perform ABC inventory classification analysis.
"""

from abc import ABC

import pandas as pd


# LOAD DATA

df = pd.read_csv("data/processed/cleaned_dataset.csv")

# Fix mixed date formats (VERY IMPORTANT)
df['date'] = pd.to_datetime(df['date'], format='mixed', dayfirst=True)


# FORECASTING

df = df.sort_values(by=['store_id', 'product_name', 'date'])

df['forecast'] = (
    df.groupby(['store_id', 'product_name'])['demand_qty']
    .transform(lambda x: x.rolling(7).mean().shift(1))
)

# FINAL SORT
final_df = df.sort_values(by=['date', 'store_id', 'product_name'])

# Reset index
final_df = final_df.reset_index(drop=True)


# SAVE

final_df.to_csv("data/processed/final_forecast.csv", index=False)

print("Forecasting completed successfully")

forecast_output = final_df[
    final_df['forecast'].notna()
][
    [
        'date',
        'store_id',
        'product_name',
        'demand_qty',
        'forecast'
    ]
]


# ABC ANALYSIS

# Total demand per product

abc_df = final_df.groupby('product_name')['demand_qty'].sum().reset_index()

# Sort descending

abc_df = abc_df.sort_values(by='demand_qty', ascending=False)

# Total demand overall

total_demand = abc_df['demand_qty'].sum()

# Demand contribution %

abc_df['demand_percent'] = (
    abc_df['demand_qty'] / total_demand
)

# Cumulative %

abc_df['cumulative_percent'] = (
    abc_df['demand_percent'].cumsum()
)

# ABC Classification

def abc_category(x):

    if x <= 0.70:
        return 'A'

    elif x <= 0.90:
        return 'B'

    else:
        return 'C'

abc_df['abc_category'] = abc_df['cumulative_percent'].apply(abc_category)

# Merge back into main dataset

final_df = pd.merge(
    final_df,
    abc_df[['product_name', 'abc_category']],
    on='product_name',
    how='left'
)

# Save final dataset

final_df.to_csv(
    "data/processed/final_inventory_dataset.csv",
    index=False
)

print("ABC Analysis Completed")

abc_mapping = abc_df[['product_name', 'abc_category']]

abc_mapping.to_csv(
    "data/processed/abc_mapping.csv",
    index=False
)

print("ABC Mapping File Created")

# print(abc_df.head(20))

