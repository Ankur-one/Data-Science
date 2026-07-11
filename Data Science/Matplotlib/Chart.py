import matplotlib.pyplot as plt

x = ['Mon','Tue','Wed','Thu','Fri']
y = [12,5,17,8,16]

plt.plot(x,y)

plt.title("Bakery Sales this week")
plt.xlabel("Day of the week")
plt.ylabel("Sales per day")
plt.show()