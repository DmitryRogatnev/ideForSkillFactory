import pandas as pd 

countries_data = pd.read_csv(
    "data/countries.csv", sep=";"
)  # Загружаем данные из файла в переменную, создавая объект DataFrame
countries_data.to_csv(
    "data/countries.txt", index=False, sep=" "
)  # Выгружаем данные из DataFrame в CSV-файл и сохраняем файл в папке data

txt_df = pd.read_table(
    "data/countries.txt", sep=" ", index_col=["country"]
)  # Загружаем данные из файла в переменную, создавая объект DataFrame

data = pd.read_table('https://raw.githubusercontent.com/esabunor/MLWorkspace/master/melb_data.csv', sep=',')
display(data)