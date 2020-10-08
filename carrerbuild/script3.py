import pandas as pd
res1 = pd.read_csv('res1.csv')
res2 = pd.read_csv('res2.csv')

merged = res1.merge(res2,on='Merges',how='left')
merged.to_csv("output.csv",index=False)

df = pd.read_csv('output.csv')
df["Blank"]=""
df["Blank"]=""
df["Blank"]=""
df["Blank"]=""
df["Blank"]=""
df["Blank"]=""
df["Blank"]=""
df["Blank"]=""
df["Blank"]=""
df["Blank"]=""
df["Blank"]=""
df["Blank"]=""
df["Blank"]=""
df["Blank"]=""
df.drop(columns=['Merges'])
df = df[['Logo','Title','Location','Company','Description','Blank','ApplyLink','Jobtype','Blank','Blank','Blank','CoIndustry','Blank','CoWebsite','Blank','Blank','Blank','Blank','Blank','Blank','Skill']]
df.to_csv('csvEXAMPLE.csv',index=False)