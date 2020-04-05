import pandas as pd
import csv




df = pd.read_csv("final.csv" ,error_bad_lines=False)
df = df.loc[:, df.columns != 'stroke']
cols = df.columns.tolist()

l = dict(df.std(axis=0))
print(len(l))


df_trans = df.div(df.std(axis=0))
#print(df_trans)
df_trans.to_csv("final_transformed.csv")

#check
df_av = df["avcarbp2"].div(df["avcarbp2"].std())
print(df_av.equals(df_trans["avcarbp2"]))

with open('std_dev.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(list(l.keys()))
    writer.writerow(list(l.values()))



