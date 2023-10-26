import pandas as pd

movies_df = pd.read_csv('data/movies_data/movies.csv', sep=',')
ratings1_df = pd.read_csv('data/movies_data/ratings1.csv', sep=',')
ratings2_df = pd.read_csv('data/movies_data/ratings2.csv', sep=',')
dates_df = pd.read_csv('data/movies_data/dates.csv', sep=',')
dates_df['date'] = pd.to_datetime(dates_df['date'])
ratings_df = pd.concat([ratings1_df, ratings2_df], ignore_index=True)
ratings_df = ratings_df.drop_duplicates(ignore_index=True)
ratings_dates_df = pd.concat([ratings_df, dates_df], axis=1)
print(dates_df['date'].dt.year.value_counts())