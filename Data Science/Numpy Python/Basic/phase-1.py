import numpy as np

# arr_1d = np.array([1,2,3,4,5])
# print(arr_1d)

# arr_2d = np.array([[1,2,3],[4,5,6]])
# print(arr_2d)

#                List vs Numpy array

# py_list = [1,2,3]
# print("Python list multiplication ",py_list*2)

# np_array = np.array([1,2,3])
# print("Python arrays multiplication ", np_array*2)

# import time

# start =  time.time()
# py_list = [i*2 for i in range(10000000)]
# print("\n List operation time ", time.time() - start)

# np_array = np.arange(1000000) * 2
# print("\n Numpy opration time ",time.time() - start)


#           Creating arrays from scratch

# zeroes = np.zeros((3,4))
# print("Zeroes arrays : \n", zeroes)

# ones = np.ones((2,3))
# print("Ones arrays : \n", ones)

# full = np.full((2,2), 7)
# print("Full arrays :\n ",full)

# random = np.random.random((2,3))
# print("Random arrays : \n", random)

# sequence = np.arange(0,10,2)
# print("Sequence arrays : \n", sequence)



#               Vectors , Matrix and tensor

# vector = np.array([1,2,3])
# print("Vector : ", vector)

# matrix = np.array([[1,2,3],
#                    [4,5,6]])
# print("Matrix : ", matrix)

# tensor = np.array([[[1,2],[3,4]],
#                    [[5,6],[7,8]]])
# print("Tensor : \n", tensor)


#           Array Properties

# arr = np.array([[1,2,3],
#                [4,5,6]])
# print("Shape : \n",arr.shape)
# print("Dimension : ", arr.ndim)
# print("Size : ", arr.size)
# print("D type : ", arr.dtype)

#       Array Reshaping

arr = np.arange(12)
print("Original array : ",arr)

reshaped = arr.reshape((3,4))
print("Reshaped : \n", reshaped)