# Sorting data
# Sorting data 1 COLUMN sort_values()

# df.sort_values(by="Column Name", True/False, implace = True)


import pandas as pd

data = {
    "Name":["Ankur","Mohan","Aman"],
    "Age":[21,20,18],
    "Salary":[10000,20000,35000]
}

df = pd.DataFrame(data)
df.sort_values(by="Age",ascending=True,inplace=True)
print("Sorted age by ascending")
print(df)