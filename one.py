import pandas as pd

data = pd.read_json('data.json')

warehouse_rate = data.groupby('warehouse_name')['highway_cost'].sum()
for warehouse, rate in warehouse_rate.items():
    print(f'Склад: {warehouse}, тариф: {rate}')