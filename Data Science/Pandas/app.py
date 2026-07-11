import pandas as pd

# read data free csv file into a dataframe

# df = pd.read_csv("sales_data_sample.csv",encoding="latin")

# print(df)


pf = pd.read_excel("SampleSuperstore.xlsx")
# print(pf)


pp = pd.read_json("sample_Data.json")
print(pp)