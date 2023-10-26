import pandas as pd 
log = pd.read_csv('data/log.csv', header=None) 
log.columns = ['user_id', 'time', 'bet', 'win'] 
users = pd.read_csv('data/users.csv',sep=',', encoding='koi8-r') 
users.columns = ['user_id', 'email', 'geo'] 
users.user_id = users.user_id.apply(lambda x: x.lower())  
log = log[log.user_id != "#error"] 
log = log.dropna(subset=['time']) 
log = log.drop_duplicates(subset=['user_id', 'time']) 
log.user_id = log.user_id.str.split(" - ").apply(lambda x: x[1]) 
log['bet'] = log['bet'].fillna(0) 
log['win'] = log['win'].fillna(0) 
log['net'] = log['win']-log['bet'] 
log['time'] = log.time.apply(lambda x: str(x)[1:]) 
log["time"] = pd.to_datetime(log["time"]) 
new_df = pd.merge(log, users, on='user_id') 
new_df['bet'] = new_df['bet'].fillna(0) 
new_df['win'] = new_df['win'].fillna(0) 
def fillna_win(row): 
    if row.win > 0: 
        return row.win 
    elif row.win==0: 
        row.bet==0 
        return 0 
    else: 
        return row.win-row.bet 
new_df['win'] = new_df.apply(lambda row: fillna_win(row), axis=1) 
new_df['net'] = new_df['win'] - new_df['bet'] 
min_bet = log[log['bet'] > 0].groupby('user_id').time.min() 
min_visit = log[log['bet'] == 0].groupby('user_id').time.min() 
timedelta = min_bet - min_visit 
print(new_df[new_df.bet > 0].groupby('geo').bet.mean().max()/new_df[new_df.bet > 0].groupby('geo').bet.mean().min())