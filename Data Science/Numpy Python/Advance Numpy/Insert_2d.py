import numpy as np

arr_2d = np.array([[1,2,3],[4,5,6],[7,8,9]])
print(arr_2d)
new_2d = np.insert(arr_2d, 1, [11,55,44], axis=0)
print(new_2d)