#four type of function arguments


#(1):- 1. Default arguments
# def average(a,b):
#     print("The average is ",(a+b)/2)
# average(4,2)  


def name(fname, mname = "John",lname = "Whatson"):
    print("Hello,", fname, mname, lname)

name("Any", "Agarwal",)


#(2):- 2.Keyword Arguments
# def average(a=9, b=1):
#     print("The average is ", (a+b)/2)

# average(b=9)
# average(b=9, a=21) 


#(3):- 3.Required Aruments
# def average(a,b, c=1):
#     print("The average is ",(a+b+c)/3)

# average(5,6)  


# #(4):- 4.Variable length arguments:
# def average(*numbers):
#     sum = 0
#     for i in numbers:
#         sum = sum + i
#     print("Average is: ", sum / len(numbers))
# average(5,6)        