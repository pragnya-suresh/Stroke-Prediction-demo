import pandas as pd
import csv


df = pd.read_csv("final.csv" ,error_bad_lines=False)
df = df.loc[:, df.columns != 'stroke']
df = df.loc[:, df.columns != 'nsrrid']
cols = df.columns.tolist()
print(cols)

#categorical 
categorical_attr = ['wksblk25','wk1blk25','climb125','bathe25','rest10','modact25','lift25','climbs25','hlthlm25']

std_dev={}
for col in cols:
    if col in categorical_attr:
        std_dev[col] = 0.05
        df[col] = df[col].div(std_dev[col])
    else:
        std_dev[col] = df[col].std()
        if(std_dev[col]<0.5):
            std_dev[col] = 0.5
        df[col] = df[col].div(std_dev[col])
        
        
print("Writing to final_transformed.csv") 
df.to_csv("final_transformed.csv", index=False)


print("Writing to std_dev.csv")

with open('std_dev.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(list(std_dev.keys()))
    writer.writerow(list(std_dev.values()))



#df_trans = df.div(df.std(axis=0))
#print(df_trans)


#check
#df_av = df["ventrate"].div(df["ventrate"].std())
#print(df_av.equals(df_trans["ventrate"]))