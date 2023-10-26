import pandas as pd

def delete_columns(df, col=[]):
    for colm_name in col:
        try:
            df_colum= df[colm_name]  
        except KeyError:
            return None
    df_new = df.drop(col, axis=1)
    return df_new

customer_data = pd.DataFrame({
        'number': [0, 1, 2, 3, 4],
        'cust_id': [128, 1201, 9832, 4392, 7472],
        'cust_age': [13, 21, 19, 21, 60],
        'cust_sale': [0, 0, 0.2, 0.15, 0.3],
        'cust_year_birth': [2008, 2000, 2002, 2000, 1961],
        'cust_order': [1400, 14142, 900, 1240, 8430]
    })

print(customer_data['number'])
customer_df = delete_columns(customer_data, col=['number', 'cust_year_birth'])
print(customer_df)