import pandas as pd

def get_experience(arg):
    if arg.find("мес") != -1:
        month_count = arg[arg.find("мес")-2: arg.find("мес")-1]
        
    if arg.find("год") != -1:
        year_count = arg[arg.find("год")-2: arg.find("год")-1]
 
    if arg.find("лет") != -1:
        year_count = arg[arg.find("лет")-2: arg.find("лет")-1]
    return int(month_count) + (int(year_count) * 12)

print(get_experience('Опыт работы 8 лет 3 месяца'))         
