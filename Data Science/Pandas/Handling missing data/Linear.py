import pandas as pd

data = {
    "Time":[1,None,3,None,5],
    "Value":[10,20,30,40,50]
}

df = pd.DataFrame(data)
print('Before interpolation')
print(df)

# Interpolation
df['Time'] = df['Time'].interpolate(method="linear")

print('After interpolation')
print(df)
