# def show(n):
#     if(n == 0):
#         return
#     print(n)
#     show(n-1)

# show(5)    


#  --> Factorial
# n = int(input("Enter the number :"))
# def fact(n):
#     if(n == 0 or n == 1):
#         return 1
#     return n * fact(n-1)
    
# print("Factorial of the number :",fact(n))



def cal_sum(n):
    if(n == 0):
        return 0
    return cal_sum(n-1) + n

sum = cal_sum(10)
print(sum)  