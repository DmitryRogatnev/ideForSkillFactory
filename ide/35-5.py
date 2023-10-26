import pandas as pd

melb_data = pd.read_csv('data/melb_data.csv', sep=',')
print(melb_data.iloc[3521].get('Landsize') / melb_data.iloc[1690].get('Landsize'))
melb_data['Postcode'] = melb_data['Postcode'].astype('int64')
melb_data['Car'] = melb_data['Car'].astype('int64')
melb_data['Bedroom'] = melb_data['Bedroom'].astype('int64')
melb_data['Bathroom'] = melb_data['Bathroom'].astype('int64')
melb_data['Propertycount'] = melb_data['Propertycount'].astype('int64')
melb_data['YearBuilt'] = melb_data['YearBuilt'].astype('int64')

landsize_median = melb_data['BuildingArea'].median() 
landsize_mean =  melb_data['BuildingArea'].mean()
ryad = company = pd.DataFrame(
     [1, 2, 4, 2, 3, 2, 1, 5, 6])
print(melb_data[(melb_data['Price'] < 3000000) & (melb_data['Type'] == 'h')]['Regionname'].value_counts())
#print(melb_data['BuildingArea'].median()/melb_data['BuildingArea'].mean())