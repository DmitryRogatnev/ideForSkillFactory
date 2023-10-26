import pandas as pd

def create_medications(names, counts):
   medications = pd.Series(
    data = counts,
    index = names,
    name = 'medications')   
   return medications


def get_percent(medications, name):
    med_count = medications[name]
    all_med_count = 0
    for med in medications:
       all_med_count += med
    per = (med_count/all_med_count)*100
    return per



names=['chlorhexidine', 'cyntomycin', 'afobazol']
counts=[15, 18, 7]
medications = create_medications(names, counts)
print(medications)
print(get_percent(medications, "chlorhexidine"))