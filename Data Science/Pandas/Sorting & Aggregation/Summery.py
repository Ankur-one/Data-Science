"""df["Column Name"].mean()
df["Column Name].sum()
df["Column Name].min()
df.[column name"].max()
"""
import pandas as pd
data = {
    "Name":["Ankur","Aman","Amit"],
    "Age":[22,56,21],
    "Salary":[50000,49000,8400]
}

df = pd.DataFrame(data)

Avg_Salary = df['Salary'].mean()
print("Average Salary :",Avg_Salary)