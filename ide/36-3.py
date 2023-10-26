import pandas as pd

ufo_df = pd.read_csv('data/ufo.csv', sep=',')
ufo_df['Time'] = pd.to_datetime(ufo_df['Time'])
ufo_df.sort_values(by=['Time'])
print(ufo_df)
year_ufo_df = ufo_df['Time'].dt.year 
days_ufo_df = ufo_df[ufo_df['State'] == 'NV']['Time'].dt.day
print(days_ufo_df)
diff_days = ufo_df[ufo_df['State'] == 'NV']['Time'].diff()
print(diff_days)
num_diff_days = diff_days.dt.days 
print(num_diff_days.mean())