import pandas as pd

df = pd.read_csv(r'./devices_info.csv')
print(df)
number_of_rows = len(df.index)
print(number_of_rows)
