# pd.merge(df1,df2, on="column Name",how="type of join")

import pandas as pd

# Customer data frame
df_customers = pd.DataFrame({
    'CustomerID':[1,2,3],
    'Name':["Ankur","Mohan","Ram"]
})

# Order data frame
df_order = pd.DataFrame({
    'CustomerID':[1,2,4],
    'OrderAmount':[250,450,350]
})

# Merge
df_merge = pd.merge(df_customers,df_order, on="CustomerID",how="outer")
print("Outer join")
print(df_merge)