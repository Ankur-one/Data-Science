# plt.his(data, bins=num_of_bins, color='colorname',edgecolor='black)

import matplotlib.pyplot as plt

score = [45,67,89,56,78,92,88,60,74,81,59,66,77,90,70,85,74,62,72]



plt.hist(score,bins=8,color='Pink',edgecolor='black',label="2025 Data")

plt.xlabel('Score Range')
plt.ylabel("Number of students")
plt.title("Score Distribution of Students")
plt.legend()
plt.show()