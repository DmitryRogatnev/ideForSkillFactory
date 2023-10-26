import pandas as pd

events_df = pd.read_csv('data/events.csv', sep=',')
purchase_df = pd.read_csv('data/purchase.csv', sep=',')

user_list = list(events_df[(events_df['start_time'] < '2019-01-01') & (events_df['start_time'] >= '2018-01-01') & (events_df['event_type'] == 'registration')]['user_id'])
events_df = events_df[events_df['user_id'].isin(user_list)]
purchase_df = purchase_df[purchase_df['user_id'].isin(user_list)]

print(events_df[events_df['event_type'] == 'tutorial_start']['user_id'].nunique())
print(purchase_df['user_id'].nunique())

purchase_df['event_type'] = 'purchase'
events_df = events_df.rename(columns={"id": "event_id"})
purchase_df = purchase_df.rename(columns={"id": "purchase_id", "event_datetime": "start_time"})

total_events_df = pd.concat([events_df,purchase_df],sort=False)
total_events_df = total_events_df.reset_index(drop=True).sort_values('start_time')

user_path_df = (     total_events_df.groupby(["user_id"])["event_type"].apply(list).reset_index() )
user_path_df["event_path"] = user_path_df["event_type"].apply(lambda x: " > ".join(x))

user_paths = (
    user_path_df.groupby(["event_path"])["user_id"]
    .nunique()
    .sort_values(ascending=False)
)
#print(user_paths.head(10))


registration_df = total_events_df[total_events_df['event_type'] == 'registration']
registration_df = registration_df[["user_id", "start_time"]].rename(
    columns={"start_time": "registration_time"}
)


tutorial_start_df = total_events_df[total_events_df['event_type'] == 'tutorial_start']
tutorial_start_df_wo_duplicates = tutorial_start_df.sort_values(
    "start_time"
).drop_duplicates("user_id")
tutorial_start_df_wo_duplicates = tutorial_start_df_wo_duplicates[
    ["user_id", "tutorial_id", "start_time"]
].rename(columns={"start_time": "tutorial_start_time"})
print(total_events_df['event_type'].value_counts())


merged_df = registration_df.merge(
    tutorial_start_df_wo_duplicates, on="user_id", how="inner"
)
merged_df["timedelta"] = (
    merged_df["tutorial_start_time"] - merged_df["registration_time"]
)

tutorial_finish_df = total_events_df[total_events_df["event_type"] == "tutorial_finish"]
first_tutorial_ids = tutorial_start_df_wo_duplicates["tutorial_id"].unique()

tutorial_finish_df = tutorial_finish_df[
    tutorial_finish_df["tutorial_id"].isin(first_tutorial_ids)
]

tutorial_finish_df = tutorial_finish_df[["user_id", "start_time"]].rename(
    columns={"start_time": "tutorial_finish_time"}
)
merged_df_2 = tutorial_start_df_wo_duplicates.merge(
    tutorial_finish_df, on="user_id", how="inner"
)
merged_df_2["timedelta"] = (
    merged_df_2["tutorial_finish_time"] - merged_df_2["tutorial_start_time"]
)


level_choice_df = total_events_df[total_events_df["event_type"] == "level_choice"]
print(level_choice_df["user_id"].value_counts().mean())
level_choice_df = level_choice_df[["user_id", "start_time"]].rename(
    columns={"start_time": "level_choice_time"}
)
merged_df_3 = registration_df.merge(level_choice_df, on="user_id", how="inner")
merged_df_3["timedelta"] = (
    merged_df_3["level_choice_time"] - merged_df_3["registration_time"]
)



registered_users_count = events_df[events_df["event_type"] == "registration"][
    "user_id"
].nunique()
tutorial_start_users_count = events_df[events_df["event_type"] == "tutorial_start"][
    "user_id"
].nunique()
percent_tutorial_start_users = tutorial_start_users_count / registered_users_count
print(
    "Процент пользователей, начавших обучение (от общего числа зарегистрировавшихся): {:.2%}".format(
        percent_tutorial_start_users
    )
)

tutorial_finish_users_count = events_df[events_df["event_type"] == "tutorial_finish"][
    "user_id"
].nunique()
tutorial_completion_rate = tutorial_finish_users_count / tutorial_start_users_count
print(
    "Процент пользователей, завершивших обучение: {:.2%}".format(
        tutorial_completion_rate
    )
)

level_choice_users_count = events_df[events_df["event_type"] == "level_choice"][
    "user_id"
].nunique()
percent_level_choice_users = level_choice_users_count / registered_users_count
print(
    "Процент пользователей, выбравших уровень сложности (от общего числа зарегистрировавшихся): {:.2%}".format(
        percent_level_choice_users
    )
)

training_choice_users_count = events_df[events_df["event_type"] == "pack_choice"][
    "user_id"
].nunique()
percent_training_choice_users = training_choice_users_count / level_choice_users_count
print(
    "Процент пользователей, выбравших пакет бесплатных вопросов (от числа пользователей, которые выбрали уровень сложности): {:.2%}".format(
        percent_training_choice_users
    )
)

paying_users_count = purchase_df["user_id"].nunique()
percent_of_paying_users = paying_users_count / training_choice_users_count
print(
    "Процент пользователей, которые совершили оплату (от числа пользователей, которые воспользовались бесплатными возможностями): {:.2%}".format(
        percent_of_paying_users
    )
)

purchase_rate = paying_users_count / registered_users_count
print(
    "Процент пользователей, которые оплатили набор вопросов (от числа зарегистрировавшихся пользователей): {:.2%}".format(
        purchase_rate
    )
)