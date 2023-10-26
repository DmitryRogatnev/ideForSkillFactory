import pandas as pd

melb_df = pd.read_csv('data/melb_data_fe.csv', sep=',')
melb_df['Date'] = pd.to_datetime(melb_df['Date'], dayfirst=False)
melb_df['Quarter'] = melb_df['Date'].dt.quarter

cols_to_exclude = ['Date', 'Rooms', 'Bedroom', 'Bathroom', 'Car'] # список столбцов, которые мы не берём во внимание
max_unique_count = 150 # задаём максимальное число уникальных категорий
for col in melb_df.columns: # цикл по именам столбцов
    if melb_df[col].nunique() < max_unique_count and col not in cols_to_exclude: # проверяем условие
        melb_df[col] = melb_df[col].astype('category')

melb_dataf = melb_df.copy()
melb_dataf.sort_values(inplace=True, by=['AreaRatio'], ascending=False)
mask1 = melb_df['Type'] == 'townhouse'
mask2 = melb_df['Rooms'] > 2
melb_dataf_t = melb_df[mask1 & mask2].copy()
melb_dataf_t.sort_values(inplace=True, by=['Rooms'])
print(melb_dataf_t)
melb_dataf_t.sort_values(inplace=True, by=['Rooms', 'MeanRoomsSquare'], 
    ascending=[True, False])
mean_melb_dataf = melb_dataf.groupby('Rooms')['Price'].mean().sort_values(ascending=False)
min_r_melb_dataf = melb_dataf.groupby('Regionname')['Lattitude'].sum().sort_values(ascending=True)
d_mask1 = melb_dataf['Date'] >= pd.to_datetime('2017-05-01')
d_mask2 = melb_dataf['Date'] <= pd.to_datetime('2017-10-01')
max_price_melb_dataf = melb_dataf[d_mask1 & d_mask2]
max_price_melb_datafr = melb_dataf.groupby('SellerG')['Price'].sum().sort_values(ascending=False)
pivot_melb_dataf = melb_df.pivot_table(values='BuildingArea',
                                       index='Type',
                                       columns='Rooms')
pivot_price_melb_dataf = melb_df.pivot_table(values='Price',
                                       index='SellerG',
                                       columns='Type',
                                       aggfunc='median')

print(pivot_price_melb_dataf)