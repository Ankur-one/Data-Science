import numpy as np


#               Numpy Array Operations

# arr = np.array([1,2,3,4,5,6,7,8,9])
# print("Basic Slicing : ", arr[2:8])
# print("With Step", arr[1:6:2])
# print("Negative Indexing : ", arr[-3])

# arr_2d = np.array([[1,2,3],
#                    [4,5,6],
#                    [7,8,9]])
# print("Specific element : \n",arr_2d[1,2])
# print("Entire row : \n",arr_2d[1])
# print("Entire column : \n", arr_2d[:,1])


# #           Sorting
# unsorted = np.array([3,8,5,9,1,0,2,7,4])
# print("Sorted Array : \n", np.sort(unsorted))

# arr_2d = np.array([[4,2],[2,1],[1,4]])
# print("Sored 2d Array : \n",np.sort(arr_2d, axis=0))


#           Filter

# numbers = np.array([1,2,3,4,5,6,7,8,9,11])
# even_number = numbers[numbers % 2 == 0]
# print("Even Numbers : ",even_number)


#       Filter with mask

# numbers = np.array([1,2,3,4,5,6,7,8,9,11])
# mask = numbers > 5
# print("Numbers greater than five : ",numbers[mask])



#       Fancy indexing vs np.where()


# numbers = np.array([1,2,3,4,5,6,7,8,9,11])
# indices = [0,2,4]
# print(numbers[indices])

# where_result = np.where(numbers > 5)
# print("NP Where ", numbers[where_result])


#           Adding and Removing

# arr1 = np.array([1,2,3])
# arr2 = np.array([4,5,6])

# comnined_array = np.concatenate((arr1, arr2))
# print(comnined_array)


#       Array Compatbality


arr1 = np.array([1,2,3])
arr2 = np.array([4,5,6])
arr3 = np.array([7,8,9])

print("Compatability shapes : ", arr1.shape == arr2.shape)

original = np.array([[1,2],[3,4]])
new_row = np.array([[5,6]])

with_new_row = np.vstack((original, new_row))
print("Original Arrray : \n",original)
print("Added new Rows : \n",with_new_row)

new_col = np.array([[7],[8]])
with_new_col = np.hstack((original,new_col))
print("Added new column : \n",with_new_col)


arr = np.array([1,2,3,4,5])
deleted = np.delete(arr,2)
print("DEleted : ", deleted)