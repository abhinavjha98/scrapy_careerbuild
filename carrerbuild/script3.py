import pandas as pd
res1 = pd.read_csv('res1.csv')
res2 = pd.read_csv('res2.csv')

merged = res1.merge(res2,on='Merges')
merged.to_csv("output.csv",index=False)