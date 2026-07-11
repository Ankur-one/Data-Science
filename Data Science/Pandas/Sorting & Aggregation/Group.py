import pandas as pd

data = {
    "Name":["Ankur","Aman","Amit"],
    "Age":[22,56,21],
    "Salary":[50000,49000,8400]
}

df = pd.DataFrame(data)
grouped = df.groupby("Age")["Salary"].sum()
print(grouped)