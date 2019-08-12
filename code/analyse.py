import pandas as pd

df = pd.read_csv('../results/carinfo.csv')

df = df.set_index(['品牌'])
print(df)
print(df.index)
