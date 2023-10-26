import pandas as pd

def create_companyDF(income, expenses, years):
    company = pd.DataFrame(
    {'income': income,
    'expenses': expenses} )
    company.index = years
    return company


def get_profit(df, year=None):
    try:
        df_year = df.loc[year]  
    except KeyError:
        return None
    df_income = df['income']
    df_expenses = df['expenses']
    revenu = 0
    revenu = df_income.get(year) - df_expenses.get(year)
    return revenu
       

income = [478, 512, 196]
expenses = [156, 130, 270]
years = [2018, 2019, 2020]
#company =  create_companyDF(income, expenses, years)

company = pd.read_csv('https://raw.githubusercontent.com/esabunor/MLWorkspace/master/melb_data.csv') #pd.read_csv('company.csv', sep=';')
#company.to_csv('company.csv', index=False, sep=';')


print(company)
#print(get_profit(company,2020))

