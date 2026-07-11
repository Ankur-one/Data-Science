import numpy as np

arr = np.array([1,2,np.nan,4,np.nan,np.nan,7])

cleaned_arr = np.nan_to_num(arr,nan=100)

print(cleaned_arr)