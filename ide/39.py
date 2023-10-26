import pandas as pd
def fillna_win(row): 
    if (row.bet == 0) & (row.win == 0):
        row.win = 0
    elif (row.bet != 0) & (row.win == 0):        
        row.win = 0 - row.bet
    return row  

def profession_code(s):
    if s == 'Рабочий':
        return 0
    elif s == 'Менеджер':
        return 1
    else:
        return 2
    
def age_category(age):
    if age < 23:
        return "молодой"
    elif (age >= 23) & (age < 35):
        return "средний"
    elif age >= 35:
        return "зрелый"
    
def cut_user_id(user_id):
    if user_id == '#error':
        return ""
    else:
        return user_id[24:]
    
def cut_time(time):
        return str(time).replace('[', '')
    
log_df = pd.read_csv('data/log.csv', sep=',', header=None)
log_df.columns = ["user_id", "time", "bet", "win"]
#log_df = log_df.drop_duplicates(subset=['user_id', 'time'])
log_df.bet = log_df.bet.fillna(0)
log_df.win = log_df.win.fillna(0)
#new_win = log_df.apply(lambda row: fillna_win(row), axis=1)
#log_df['win'] = new_win.win
log_df['net'] = log_df[log_df.win > 0].win - log_df[log_df.win > 0].bet
log_df['net'] = log_df.win - log_df.bet
min_bet_amount = log_df[log_df.bet == log_df.bet.min()].bet.value_counts()
users_df = pd.read_csv('data/users.csv',sep=',', encoding='koi8-r')
users_df.columns = ["user_id", "mail", "geo"]
users_df.user_id = users_df.user_id.str.lower()
sample_df = pd.read_csv('data/sample.csv',sep=',')

log2 = log_df.query("bet<2000 & win>0")
sample3 = sample_df[sample_df.City.str.contains("о", na=False)]
log_wo_errors = log_df[~log_df.user_id.str.contains("error", na=False)]

sample2 = sample_df.copy()
#print(sample2)
sample2['Age'] = sample2.Age.apply(lambda x: x+1)
sample2['City'] = sample2.City.apply(lambda x: str(x).lower())
sample2['Profession'] = sample2.Profession.apply(profession_code)
sample2['Age_category'] = sample2.Age.apply(age_category)
log3 = log_df.copy()
log3["user_id"] = log3.user_id.apply(cut_user_id)
log3["time"] = log3.time.apply(lambda x: str(x)[1:] if str(x)[0] == '[' else x)
log3["time"] = pd.to_datetime(log3["time"])
users_log_df = pd.merge(log3, users_df, on='user_id' )
#print(log_df[(log_df.net < 0) & ((log_df.bet > 0))].shape[0]/log_df[(log_df.bet > 0)].shape[0])
#print(log_df[(log_df.net > 0) & ((log_df.bet > 0))].shape[0]/log_df[(log_df.bet > 0)].shape[0])
#print(min_bet_amount)
users_w_bet_set= set(users_log_df[users_log_df.bet > 0].user_id)
users_w_bet_df= users_log_df[users_log_df.user_id.isin(users_w_bet_set)]
users_group_df = users_log_df.groupby("user_id")
users_first_visit_df = users_log_df[users_log_df.bet == 0].groupby("user_id").time.min()
users_first_visit_df.columns = ["user_id", "first_visit_time"]
users_first_bet_df = users_log_df[users_log_df.bet > 0].groupby("user_id").time.min()
users_first_bet_df.columns = ["user_id", "first_bet_time"]
users_first_merged_df = pd.merge(users_first_visit_df, users_first_bet_df, on='user_id' )
users_first_merged_df.columns = ["first_visit_time", "first_bet_time"]
users_first_merged_df["time_amount"] = users_first_merged_df.first_bet_time - users_first_merged_df.first_visit_time
print(users_first_merged_df.time_amount.mean())
