# Generated simulated quick commerce operational dataset
# including demand, inventory, fulfillment,
# and weather-influenced retail behavior.

import pandas as pd
import numpy as np
import requests
import os
from dotenv import load_dotenv

# Create folders if they don't exist
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# LOAD API KEY
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = "Bangalore"


# SETUP

np.random.seed(42)

START_DATE = "2025-01-01"
END_DATE = "2025-06-30"
STORES = [101, 102, 103]

# PRODUCT TABLE

products = [
    ("P01", "Milk", "Dairy", 60),
    ("P02", "Curd", "Dairy", 50),
    ("P03", "Butter", "Dairy", 40),
    ("P04", "Paneer", "Dairy", 35),

    ("P05", "Bread", "Bakery", 55),
    ("P06", "Buns", "Bakery", 45),
    ("P07", "Cake", "Bakery", 30),

    ("P08", "Chips", "Snacks", 40),
    ("P09", "Biscuits", "Snacks", 35),
    ("P10", "Namkeen", "Snacks", 30),

    ("P11", "Coke", "Beverages", 30),
    ("P12", "Juice", "Beverages", 35),
    ("P13", "Soda", "Beverages", 25),
    ("P14", "Energy Drink", "Beverages", 20),

    ("P15", "Eggs", "Essentials", 50),
    ("P16", "Oil", "Essentials", 30),
    ("P17", "Rice", "Essentials", 45),
    ("P18", "Atta", "Essentials", 40)
]

dim_product = pd.DataFrame(products, columns=[
    "product_id", "product_name", "category", "base_demand"
])

dim_product.to_csv("data/raw/dim_product.csv", index=False)


# GENERATE DEMAND DATA

dates = pd.date_range(start=START_DATE, end=END_DATE)

data = []

for date in dates:
    for store in STORES:
        for pid, pname, category, base in products:

            demand = base

            if date.weekday() >= 5:
                demand *= 1.2

            if category == "Snacks":
                demand *= np.random.uniform(0.8, 1.5)
            elif category == "Dairy":
                demand *= np.random.uniform(0.9, 1.1)
            elif category == "Beverages":
                demand *= np.random.uniform(0.85, 1.3)

            demand += np.random.randint(-5, 6)
            demand = max(0, int(demand))

            inventory = demand + np.random.randint(-15, 10)

            fulfilled = min(demand, inventory)
            stockout = 1 if demand > inventory else 0

            data.append([
                date, store, pid, pname, category,
                demand, inventory, fulfilled, stockout
            ])

fact_df = pd.DataFrame(data, columns=[
    "date", "store_id", "product_id", "product_name", "category",
    "demand_qty", "inventory_qty", "fulfilled_qty", "stockout_flag"
])

fact_df.to_csv("data/raw/fact_demand_inventory.csv", index=False)


# WEATHER DATA

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    
    response = requests.get(url)
    data = response.json()

    # Check if API failed
    if "main" not in data:
        print("API ERROR:", data)
        return 25, "Clear"   # fallback values

    return data['main']['temp'], data['weather'][0]['main']

temp_base, weather_base = get_weather()

weather_types = ["Clear", "Clouds", "Rain"]

weather_data = []

for date in dates:
    temp = temp_base + np.random.uniform(-3, 3)
    weather = np.random.choice(weather_types)
    weather_data.append([date, temp, weather])

weather_df = pd.DataFrame(weather_data, columns=[
    "date", "temperature", "weather_type"
])

weather_df.to_csv("data/raw/weather_data.csv", index=False)


# MERGE

fact_df['date'] = pd.to_datetime(fact_df['date'])
weather_df['date'] = pd.to_datetime(weather_df['date'])

final_df = pd.merge(fact_df, weather_df, on="date", how="left")

final_df.to_csv("data/processed/final_dataset.csv", index=False)

print("SUCCESS: Data generated")

print(final_df.head(20))