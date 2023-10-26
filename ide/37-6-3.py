import pandas as pd
import os as os

def concat_user_files(path):
    list_files = os.listdir(path)
    list_files.sort()
    main_df = pd.DataFrame()
    for file in list_files:
        temp_df = pd.read_csv( (path + '/' + file), sep=',')
        main_df = pd.concat([main_df, temp_df], ignore_index=True)
        main_df = main_df.drop_duplicates(ignore_index=True)
    return main_df

test_df = concat_user_files('data/movies_data')
print(test_df)