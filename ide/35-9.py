import pandas as pd

student_data = pd.read_csv('data/students_performance.csv', sep=',') 
student_w_A= student_data[student_data['race/ethnicity'] == 'group A']['writing score'].median()
student_w_C = student_data[student_data['race/ethnicity'] == 'group C']['writing score'].mean()
print( student_w_A - student_w_C )
#print( student_data['parental level of education'].value_counts(normalize=True)*100 )