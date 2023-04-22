import pandas as pd

df = pd.read_csv('./assets/quotes4.csv', sep=',')

print(df['GENRE'].unique())

# df = df[df['GENRE'] != 'power']
# df.to_csv('./assets/quotes4.csv', sep=',')

