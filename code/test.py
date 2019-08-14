import pandas as pd

a = [1,1,1,2,2,2,0,3,3,4]

s = pd.Series(a).value_counts()
print(s)

b = pd.DataFrame([[1,3,3],[4,2,3],[7,1,3]], columns=['a','b','c'])
print(b.set_index(['c','b']).unstack())
# print(b[b < 3])
# print(b.loc[[0,1]])
a = pd.Series([1,2,3,4,5])
a[5] = 6
aa = pd.DataFrame(a)
c = pd.Series([2,2,2,2,2,2])
aa[1] = c
print(aa)

if []:
    print('1')
else:
    print('2')
