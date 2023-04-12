import pandas as pd

df = pd.read_csv('assets/quotes4.csv' ,sep=',')

# with open('assets/list to change.txt', 'r') as f:
# 	genres = f.readlines()

# changed = df.replace([i.strip().split(' - ')[0] for i in genres], [i.strip().split(' - ')[1] for i in genres])

changed = df.drop(columns=['Unnamed: 0.1', 'Unnamed: 0'])
print(changed)

changed.to_csv('quotes5.csv')