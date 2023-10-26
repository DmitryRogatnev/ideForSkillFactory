import pandas as pd

def get_weekend(weekday):
    if weekday in (5, 6):
        return 1
    else:
        return 0

melb_data = pd.read_csv('data/melb_data.csv', sep=',')
melb_df = melb_data.copy()
melb_df.head()
melb_df = melb_df.drop(['index', 'Coordinates'], axis=1)
melb_df.head()
total_rooms = melb_df['Rooms'] + melb_df['Bedroom'] + melb_df['Bathroom']
melb_df['MeanRoomsSquare'] = melb_df['BuildingArea'] / total_rooms
diff_area = melb_df['BuildingArea'] - melb_df['Landsize']
sum_area = melb_df['BuildingArea'] + melb_df['Landsize']
melb_df['AreaRatio'] = diff_area/sum_area
melb_df['Date'] = pd.to_datetime(melb_df['Date'], dayfirst=True)
week_sale_df = melb_df['Date'].dt.weekday
melb_df['WeekdaySale'] = week_sale_df
melb_df['Weekend'] = melb_df['WeekdaySale'].apply(get_weekend)
print(melb_df[(melb_df['Weekend'] == 1)]['Price'].mean())
most_popular_sellers = melb_df['SellerG'].value_counts().nlargest(49).index
print(most_popular_sellers)
melb_df['SellerG'] = melb_df['SellerG'].apply(lambda x: x if x in most_popular_sellers else 'Other')
print(melb_df['SellerG'].value_counts())

cols_to_exclude = ['Date', 'Rooms', 'Bedroom', 'Bathroom', 'Car'] # список столбцов, которые мы не берём во внимание
max_unique_count = 150 # задаём максимальное число уникальных категорий
for col in melb_df.columns: # цикл по именам столбцов
    if melb_df[col].nunique() < max_unique_count and col not in cols_to_exclude: # проверяем условие
        melb_df[col] = melb_df[col].astype('category')

print(melb_df.info())


most_popular_suburb = melb_df['Suburb'].value_counts().nlargest(119).index
melb_df['Suburb'] = melb_df['Suburb'].apply(lambda x: x if x in most_popular_suburb else 'Other')
melb_df['Suburb'] = melb_df['Suburb'].astype('category')

print(melb_df.info())