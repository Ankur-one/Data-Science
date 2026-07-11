import pandas as pd

# Adding columns
data = {
    "Name":['Ram','Om','Mohan','Ankur','Ankush'],
    "Age": [18,25,32,22,25],
    "Salary":[50000,30000,55000,85000,56000],
    "Performanace Score":[85,65,88,89,75]
}

df = pd.DataFrame(data)
print(df)
#  Square brackets of["columns_name"] = some_Data
print("Bonus Included \n")
df["Bonus"] = df['Salary'] * 0.1
print(df)

# using insert

df.insert(0,"Employee_ID",[101,102,103,104,105])
print(df)