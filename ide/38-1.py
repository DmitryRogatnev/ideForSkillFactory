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

print(purchase_df)

user_path_df = (     total_events_df.groupby(["user_id"])["event_type"].apply(list).reset_index() )
user_path_df["event_path"] = user_path_df["event_type"].apply(lambda x: " > ".join(x))

user_paths = (
    user_path_df.groupby(["event_path"])["user_id"]
    .nunique()
    .sort_values(ascending=False)
)

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


merged_df = registration_df.merge(
    tutorial_start_df_wo_duplicates, on="user_id", how="inner"
)
merged_df["tutorial_start_time"] = pd.to_datetime(merged_df["tutorial_start_time"], dayfirst=False)
merged_df["registration_time"] = pd.to_datetime(merged_df["registration_time"], dayfirst=False)
merged_df["timedelta"] =  merged_df["tutorial_start_time"] - merged_df["registration_time"]
print(merged_df.info())

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
merged_df_2["tutorial_finish_time"] = pd.to_datetime(merged_df_2["tutorial_finish_time"], dayfirst=False)
merged_df_2["tutorial_start_time"] = pd.to_datetime(merged_df_2["tutorial_start_time"], dayfirst=False)
merged_df_2["timedelta"] = (
    merged_df_2["tutorial_finish_time"] - merged_df_2["tutorial_start_time"]
)

level_choice_df = total_events_df[total_events_df["event_type"] == "level_choice"]
print(level_choice_df["user_id"].value_counts().mean())
level_choice_df = level_choice_df[["user_id", "start_time"]].rename(
    columns={"start_time": "level_choice_time"}
)
merged_df_3 = registration_df.merge(level_choice_df, on="user_id", how="inner")
merged_df_3["level_choice_time"] = pd.to_datetime(merged_df_3["level_choice_time"], dayfirst=False)
merged_df_3["registration_time"] = pd.to_datetime(merged_df_3["registration_time"], dayfirst=False)
merged_df_3["timedelta"] = (
    merged_df_3["level_choice_time"] - merged_df_3["registration_time"]
)

pack_choice_df = total_events_df[total_events_df["event_type"] == "pack_choice"]
print(pack_choice_df["user_id"].value_counts().mean())
pack_choice_df = pack_choice_df[["user_id", "start_time"]].rename(
    columns={"start_time": "pack_choice_time"}
)
merged_df_4 = level_choice_df.merge(pack_choice_df, on="user_id", how="inner")
merged_df_4["level_choice_time"] = pd.to_datetime(merged_df_4["level_choice_time"], dayfirst=False)
merged_df_4["pack_choice_time"] = pd.to_datetime(merged_df_4["pack_choice_time"], dayfirst=False)
merged_df_4["timedelta"] = (
    merged_df_4["pack_choice_time"] - merged_df_4["level_choice_time"]
)

purchase_dataf = total_events_df[total_events_df["event_type"] == "purchase"]
print(purchase_dataf["user_id"].value_counts().mean())
purchase_dataf = purchase_dataf[["user_id", "start_time"]].rename(
    columns={"start_time": "purchase_time"}
)
merged_df_5 = pack_choice_df.merge(purchase_dataf, on="user_id", how="inner")
merged_df_5["purchase_time"] = pd.to_datetime(merged_df_5["purchase_time"], dayfirst=False)
merged_df_5["pack_choice_time"] = pd.to_datetime(merged_df_5["pack_choice_time"], dayfirst=False)
merged_df_5["timedelta"] = (
    merged_df_5["purchase_time"] - merged_df_5["pack_choice_time"]
)

users_with_finished_tutorial = total_events_df[
    total_events_df["event_type"] == "tutorial_finish"
]["user_id"].unique()
print(len(users_with_finished_tutorial))

users_with_started_tutorial = total_events_df[
    total_events_df["event_type"] == "tutorial_start"
]["user_id"].unique()
set_users_with_started_tutorial = set(users_with_started_tutorial)
set_users_not_finished_but_started_tutorial = (
    set_users_with_started_tutorial.difference(set(users_with_finished_tutorial))
)

print(len(set_users_with_started_tutorial))
print(len(set_users_not_finished_but_started_tutorial))
print(
    len(set_users_with_started_tutorial) - len(set(users_with_finished_tutorial))
    == len(set_users_not_finished_but_started_tutorial)
)

all_users = total_events_df["user_id"].unique()
set_all_users = set(all_users)
set_users_not_started_tutorial = set_all_users.difference(
    set_users_with_started_tutorial
)
print(len(set_users_not_started_tutorial))
print(
    len(set_all_users) - len(set_users_with_started_tutorial)
    == len(set_users_not_started_tutorial)
)

purchase_df_1 = purchase_df[purchase_df["user_id"].isin(users_with_finished_tutorial)]

percent_of_purchase_1 = purchase_df_1["user_id"].nunique() / len(
    users_with_finished_tutorial
)
print(
    "Процент пользователей, которые оплатили тренировки (от числа пользователей, завершивших обучение): {:.2%}".format(
        percent_of_purchase_1
    )
)

purchase_df_2 = purchase_df[
    purchase_df["user_id"].isin(set_users_not_finished_but_started_tutorial)
]
print(purchase_df_2["user_id"].nunique())
percent_of_purchase_2 = purchase_df_2["user_id"].nunique() / len(
    set_users_not_finished_but_started_tutorial
)
print(
    "Процент пользователей, которые оплатили тренировки (от числа пользователей, начавших обучение, но не завершивших): {:.2%}".format(
        percent_of_purchase_2
    )
)

purchase_df_3 = purchase_df[
    purchase_df["user_id"].isin(set_users_not_started_tutorial)
]
print(purchase_df_3["user_id"].nunique())
percent_of_purchase_3 = purchase_df_3["user_id"].nunique() / len(
    set_users_not_started_tutorial
)
print(
    "Процент пользователей, которые оплатили тренировки (от числа пользователей, не начавших обучение, но не завершивших): {:.2%}".format(
        percent_of_purchase_3
    )
)

print(purchase_df_3['amount'].mean())