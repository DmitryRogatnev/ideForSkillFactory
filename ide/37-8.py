import pandas as pd
import re 

def get_year_release(arg):
    #находим все слова по шаблону "(DDDD)"
    candidates = re.findall(r'\(\d{4}\)', arg) 
    # проверяем число вхождений
    if len(candidates) > 0:
        #если число вхождений больше 0,
	#очищаем строку от знаков "(" и ")"
        year = candidates[0].replace('(', '')
        year = year.replace(')', '')
        return int(year)
    else:
        #если год не указан, возвращаем None
        return None

movie_rating_df = pd.read_csv('data/ratings_movies.csv', sep=',')
movie_rating_df['date'] = pd.to_datetime(movie_rating_df['date'])
movie_rating_df['year_release'] = movie_rating_df['title'].apply(get_year_release)
movie_rating_df['year_rating'] = movie_rating_df['date'].dt.year
mask1 = movie_rating_df['year_release'] == 2018
movie_rating_countdataf = movie_rating_df[mask1].groupby('genres').count()
movie_rating_countdataf['mrating'] = movie_rating_df.groupby('genres')['rating'].mean().sort_values(ascending=False)
#movie_rating_meargeddataf = movie_rating_countdataf.merge(movie_rating_meanratingdataf, how='inner') 
pivot_movie_rating_df = movie_rating_df.pivot_table(
    values = 'rating', 
    index='year_release',
    columns='genres',
    aggfunc='mean',
    fill_value=0 )
print(pivot_movie_rating_df.loc[2010]['Action|Adventure|Animation|Children|Comedy|IMAX'])