"""
Calculate safety stock, reorder points,
and inventory replenishment indicators.
"""

import pandas as pd

df = pd.read_csv("data/processed/final_forecast.csv")

df['date'] = pd.to_datetime(df['date'])

# CALCULATE DEMAND VARIABILITY
demand_stats = df.groupby(['store_id','product_name']).agg({
    'demand_qty': ['mean','std']
}).reset_index()

demand_stats.columns = ['store_id','product_name','avg_demand','std_demand']

# DEFINE SERVICE LEVEL
service_level = 1.65   # ~95% service level

# CALCULATE SAFETY STOCK
demand_stats['safety_stock'] = service_level * demand_stats['std_demand']

#DEFINE LEAD TIME
lead_time = 2   # days (assumption)

# CALCULATE REORDER POINT
demand_stats['reorder_point'] = (
    demand_stats['avg_demand'] * lead_time
) + demand_stats['safety_stock']


# MERGE BACK
final_df = pd.merge(
    df,
    demand_stats,
    on=['store_id','product_name'],
    how='left'
)

# INVENTORY DECISION FLAG
final_df['reorder_flag'] = (
    final_df['inventory_qty'] < final_df['reorder_point']
).astype(int)

# Remove duplicate columns
final_df = final_df.loc[:, ~final_df.columns.duplicated()]

# Save final dataset
final_df.to_csv(
    "data/processed/final_inventory_dataset.csv",
    index=False
)

print("Final dataset saved successfully")

print("Inventory decision calculation completed successfully")
  



