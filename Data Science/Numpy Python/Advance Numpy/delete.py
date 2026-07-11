# np.delete(arr, index, axis=none)
# flatern array


import numpy as np

arr = np.array([1,2,3,4,5,6,7,8,9])
print(arr)
new_arr = np.delete(arr, 4)
print(new_arr)