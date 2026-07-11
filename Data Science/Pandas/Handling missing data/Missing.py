import pandas as pd


data = {
    "Name":['Ram','Om','Mohan','Ankur','Ankush'],
    "Age": [18,25,32,22,25],
    "Salary":[50000,30000,55000,85000,56000],
    "Performanace Score":[85,65,88,89,75]
}

df = pd.DataFrame(data)
print(df)


print(df.isnull().sum())