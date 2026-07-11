"""
vertically - (rows wise)
Horizontaly - (column wise)

pd.concate([df1,df2], axis = 0, ignore_index=True)

[df1,df2] = 
axis=1

ignore_index = True
"""

import pandas as pd

df_Region1 = pd.DataFrame({
    'CustomerID':[1,2,3],
    'Name':["Ankur","Mohan","Ram"]
})

df_Region2 = pd.DataFrame({
    'CustomerID':[4,6,7],
    'Name':["Amit","Sohan","Rama"]
})

# Concenate vertically
df_concat = pd.concat([df_Region1,df_Region2], ignore_index=True)
print(df_concat)