import pandas as pd
data = {
    "Name":['Ram','Shayam','Mohan'],
    "Age":[18,25,35],
    "City":["Patna","Sonpur","Hajipur"]
}


df = pd.DataFrame(data)
print(df)

# df.to_csv("Output.csv",index=False) # save in csv file

# df.to_excel("Data.xlsx", index=False) # savein excel file

df.to_json("Name.json")