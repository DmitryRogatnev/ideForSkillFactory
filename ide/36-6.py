import pandas as pd

def get_weekend(weekday):
    if weekday in (5, 6):
        return 1
    else:
        return 0
    
def get_daytime(hour):
    if hour in list(range(0,7)):
        return 'night'
    elif hour in list(range(7,13)):
        return 'morning'
    elif hour in list(range(13,19)):
        return 'day'
    elif hour in list(range(19,24)):
        return 'evening'

citibike_data = pd.read_csv('data/citibike-tripdata.csv', sep=',')
citibike_df = citibike_data.copy()
citibike_df = citibike_df.drop(['start station id', 'end station id'], axis=1)
citibike_df['starttime'] = pd.to_datetime(citibike_df['starttime'])
citibike_df['stoptime'] = pd.to_datetime(citibike_df['stoptime'])
trip_duration = citibike_df['stoptime'] - citibike_df['starttime']
citibike_df['trip duration'] = trip_duration.dt.seconds
age = 2018 - citibike_df['birth year']
citibike_df['age'] = age 
citibike_df = citibike_df.drop(['birth year'], axis=1)
citibike_df['weekend'] = citibike_df['starttime'].dt.weekday.apply(get_weekend)
citibike_df['time_of_day'] = citibike_df['starttime'].dt.hour.apply(get_daytime)
print(citibike_df['time_of_day'].value_counts())