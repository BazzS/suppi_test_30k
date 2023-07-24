import pandas as pd

data = pd.read_json('data.json')

order_profit = {'order_id': [], 'order_profit': []}

for _, row in data.iterrows():
    order_id = row['order_id']
    products = row['products']
    highway_cost = row['highway_cost']
    total_profit = 0

    for product in products:
        price = product['price']
        quantity = product['quantity']
        profit = price * quantity + highway_cost
        total_profit += profit

    order_profit['order_id'].append(order_id)
    order_profit['order_profit'].append(total_profit)

order_profit_table = pd.DataFrame(order_profit)
average_profit = order_profit_table['order_profit'].mean()

print(order_profit_table)
print("\nСредняя прибыль по заказам:", average_profit)