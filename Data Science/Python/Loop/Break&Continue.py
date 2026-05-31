# for i in range(12):
#     if(i == 10):
#         break
#     print("5 x", i+1, "=", 5 * (i+1))

# print("Loop ko chor ka nikal jao")

# for i in range(12):
#     if(i == 10):
#         print("Skip the iteration")
#         continue
#     print("5 x", i+1, "=", 5 * (i+1))

# Break
# i = 0
# while i <= 5:
#     if(i == 3):
#         i+=1
#         break
#     print(i)
#     i += 1


# Continue
# i = 0
# while i <=5 :
#     if(i == 3):
#         i += 1
#         continue
#     print(i)
#     i += 1


# Pass
count = 5
while count > 0:
    if count == 3:
        pass
    else:
        print(count)
    count -= 1