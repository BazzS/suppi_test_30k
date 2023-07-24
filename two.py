import pandas as pd

data = pd.read_json('data.json')
data = pd.json_normalize(data.to_dict(orient='records'), record_path='products',
                         meta=['order_id', 'warehouse_name', 'highway_cost'])

data['income'] = data['price'] * data['quantity']
data['expenses'] = data['highway_cost'] * data['quantity']
data['profit'] = data['income'] - data['expenses']

product_stats = data.groupby('product').agg(
    quantity=('quantity', 'sum'),
    income=("income", "sum"),
    expenses=("expenses", "sum"),
    profit=("profit", "sum")
)

print(product_stats)
