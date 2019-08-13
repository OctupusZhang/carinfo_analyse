import pandas as pd

a = [1,1,1,2,2,2,0,3,3,4]

s = pd.Series(a).value_counts()
print(s)

b = pd.DataFrame([[1,2,3],[4,5,6]])
b[3] = [7,8,9]
print(b)
# print(b[b < 3])
# print(b.loc[[0,1]])

