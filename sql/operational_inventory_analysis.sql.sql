-- QUICK COMMERCE INVENTORY OPTIMIZATION PROJECT
-- SQL Operational & Inventory Analysiscreate database quick_commerce;
-- DATABASE SETUP

create database quick_commerce;

use quick_commerce;

rename table final_inventory_dataset to inventory_table;

-- OPERATIONAL KPI ANALYSIS

select * from inventory_table;

-- Total Operational Demand
#How much demand are we getting?
select sum(demand_qty) as Total_Demand from inventory_table;

-- Total Fulfilled Demand
#How much demand are we fulfilling?
select sum(fulfilled_qty) as Demand_Fulfilled from inventory_table;

-- Stockout Exposure Rate
#How often are we failing customers?
select avg(stockout_flag) * 100 as Stockout_rate from inventory_table;

-- Lost Sales Analysis
# How much revenue are we losing?
select sum(gap) as Lost_Sales from inventory_table;

-- PRODUCT RISK ANALYSIS

-- High-Risk Products
#Which products are operationally risky?    (High-risk SKUs)
select product_name, sum(stockout_flag) as stockouts 
from inventory_table
group by  product_name
order by stockouts desc;

-- CATEGORY PERFORMANCE ANALYSIS
# Which categories perform badly?
select category, avg(fill_rate)*100 as avg_fill_rate, 
sum(gap) as lost_sales 
from inventory_table
group by category;

-- STORE PERFORMANCE ANALYSIS
# Which stores are inefficient?
select store_id, 
avg(fill_rate)*100 as avg_fill_rate,
sum(gap) as lost_sales 
from inventory_table
group by store_id;

-- FORECAST ACCURACY ANALYSIS
# Accuracy of forecasting?
select product_name, 
avg(abs(demand_qty - forecast)) as forecast_error
from inventory_table
group by product_name;

-- REPLENISHMENT ANALYSIS
# Which products need replenishment? 
select store_id,
product_name, 
inventory_qty,
reorder_point
from inventory_table
where reorder_flag = 1;

-- DEMAND TREND ANALYSIS
#How demand changes over time?
select month, 
sum(demand_qty) as total_demand
from inventory_table
group by month
order by month;

-- WEATHER IMPACT ANALYSIS
#Does weather affect demand?
select weather_type,
avg(demand_qty) as avg_demand_qty
from inventory_table
group by weather_type;


-- ABC INVENTORY ANALYSIS
alter table inventory_table 
add column abc_category varchar(10); 

create table abc_mapping (
    product_name VARCHAR(50),
    abc_category VARCHAR(5));


update inventory_table it
join abc_mapping am
on it.product_name = am.product_name
set it.abc_category = am.abc_category;


select product_name, abc_category from inventory_table;

select  product_name,
    demand_qty,
    inventory_qty,
    forecast,
    safety_stock,
    reorder_point,
    reorder_flag from inventory_table;



