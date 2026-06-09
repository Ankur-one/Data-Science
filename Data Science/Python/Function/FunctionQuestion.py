#  -> Sum of two number
# def calc_sum(a,b):
#     sum = a+b
#     print(sum)
#     return sum

# calc_sum(5,9)


#   -> Average of 3 number
# def cal_avg(a,b,c):
#     avg = (a + b + c) / 3
#     print(avg)
#     return avg

# cal_avg(9,8,2) 


#   -->  WAP to print the length of a list.(list is the parameter)

# cities = ["Delhi", "Mumbai", "Patna", "Kolkata", "pune"]

# def print_len(list):
#     print(len(list))

# print_len(cities)


#   -->  WAP to print the elements of a list in a single line.(list is the parameter)

# cities = ["Delhi", "Mumbai", "Patna", "Kolkata", "pune"]

# def print_len(list):
#     print(len(list))

# def print_list(list):
#     for item in list:
#         print(item, end=" ")

# print_list(cities)    

#   --> WAP to find the factorial of n.(nis the parameter)

# n = 5
# fact = 1
# for i in range(1, n+1):
#     fact *= i
#     print(fact)

    #   with the help of function
# n = 5
# def cal_fact(n):
#     fact = 1
#     for i in range(1, n+1):
#         fact *= i
#     print(fact)
# cal_fact(8)  


# WAP to convert USD to INR
def converator(USD_val):
    INR_val = USD_val * 83
    print(USD_val, "USD =", INR_val, "INR")

converator(100)