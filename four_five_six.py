import pandas as pd


data = pd.read_json('data.json')


summary = {
    'product': [],
    'warehouse_name': [],
    'quantity': [],
    'income': [],
    'expenses': [],
    'profit': []
}

tariffs = {}
for _, row in data.iterrows():
    warehouse = row['warehouse_name']
    products = row['products']
    total_quantity = sum(product['quantity'] for product in products)

    if warehouse in tariffs:
        continue

    tariff = row['highway_cost'] / total_quantity
    tariffs[warehouse] = tariff

for _, row in data.iterrows():
    products = row['products']

    for product in products:
        product_name = product['product']
        warehouse = row['warehouse_name']
        price = product['price']
        quantity = product['quantity']
        expenses = tariffs[warehouse] * quantity
        profit = price * quantity + expenses

        key = f"{product_name}_{warehouse}"
        if key in summary['product']:
            index = summary['product'].index(key)
            summary['quantity'][index] += quantity
            summary['income'][index] += price * quantity
            summary['expenses'][index] += expenses
            summary['profit'][index] += profit
        else:
            summary['product'].append(key)
            summary['warehouse_name'].append(warehouse)
            summary['quantity'].append(quantity)
            summary['income'].append(price * quantity)
            summary['expenses'].append(expenses)
            summary['profit'].append(profit)

summary_table = pd.DataFrame(summary)
profit_by_warehouse = summary_table.groupby('warehouse_name')['profit'].sum().reset_index()

summary_table = pd.merge(summary_table, profit_by_warehouse, on='warehouse_name', suffixes=('', '_warehouse'))
summary_table['percent_profit_product_of_warehouse'] = (summary_table['profit'] / summary_table['profit_warehouse']) * 100
summary_table['product'] = summary_table['product'].apply(lambda x: x.split('_')[0])

print(f'Задание 4:\n{summary_table[["warehouse_name", "product", "quantity", "profit", "percent_profit_product_of_warehouse"]]}')

# 5
summary_table = summary_table.sort_values(by='percent_profit_product_of_warehouse', ascending=False)
summary_table['accumulated_percent_profit_product_of_warehouse'] = summary_table.groupby('warehouse_name')['percent_profit_product_of_warehouse'].cumsum()
print(f'Задание 5:\n{summary_table[["warehouse_name", "product", "quantity", "profit", "percent_profit_product_of_warehouse", "accumulated_percent_profit_product_of_warehouse"]]}')


# 6
def categorize_profits(percent):
    if percent <= 70:
        return 'A'
    elif 70 < percent <= 90:
        return 'B'
    else:
        return 'C'


summary_table['category'] = summary_table['accumulated_percent_profit_product_of_warehouse'].apply(categorize_profits)
print(f'Задание 6:\n{summary_table[["warehouse_name", "product", "quantity", "profit", "percent_profit_product_of_warehouse", "accumulated_percent_profit_product_of_warehouse", "category"]]}')