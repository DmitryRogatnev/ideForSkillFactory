import pandas as pd
import re 

orders_df = pd.read_csv('data\orders_and_products\orders.csv', sep=';')
orders_df['Product_ID'] = orders_df['ID товара']
orders_df = orders_df.drop(['ID товара'], axis=1)
products_df = pd.read_csv('data\orders_and_products\products.csv', sep=';')
order_products_df = orders_df.merge(products_df, on='Product_ID', how='left')

order_products_df['products_cost'] = order_products_df['Количество'] * order_products_df['Price']

print(order_products_df.groupby('ID Покупателя')['products_cost'].sum().sort_values(ascending=False))