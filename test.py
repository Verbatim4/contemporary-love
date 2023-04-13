import pandas as pd

df = pd.read_csv('assets/quotes4.csv' ,sep=',')

print(df['GENRE'].unique())