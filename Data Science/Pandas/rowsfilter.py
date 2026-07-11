import pandas as pd
data = {
    "Name":['Ram','Om','Mohan','Ankur','Ankush'],
    "Age": [18,25,32,22,25],
    "Salary":[50000,30000,55000,85000,56000],
    "Performanace Score":[85,65,88,89,75]
}

df = pd.DataFrame(data)

high_salary = df[df['Salary'] > 50000]
print("Employees with salary > 50000")
print(high_salary)

#  Filtering rows salary > 50k & age > 20

filtered = df[(df['Age'] > 20) & (df['Salary'] > 50000)]
print(f'Employees list age > 20 + Salary > 50000')
print(filtered)