import pandas as pd

countries_df = pd.DataFrame({
    'country': ['Англия', 'Канада', 'США', 'Россия', 'Украина', 'Беларусь', 'Казахстан'],
    'population': [56.29, 38.05, 322.28, 146.24, 45.5, 9.5, 17.04],
    'square': [133396, 9984670, 9826630, 17125191, 603628, 207600, 2724902]
})

country_plotn = ( countries_df['population'] * 1000000 )/countries_df['square']
countries_df['country_plotn'] = round(country_plotn, 2 )
print(round(countries_df['country_plotn'].mean(), 2 ))