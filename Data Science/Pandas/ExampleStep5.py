import pandas as pd
data = {
    "Name":['Ram','Om','Mohan','Ankur','Ankush'],
    "Age": [18,25,32,22,25],
    "Salary":[50000,30000,55000,85000,56000],
    "Performanace Score":[85,65,88,89,75]
}

df = pd.DataFrame(data)

# display the dataframe
print("Sample data frame")
print(df)

print("Names (Sinle column return series)")
name = df['Name']
print(name)

# Selecting multiple columns

subset = df[["Name","Salary"]]
print("\nSubset with Name and Salary")
print(subset)