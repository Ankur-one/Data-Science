# plt.plot(x,y, color='color_name',linestyle='line_style',linewidth=vlaue,marker='marker symbol',label='label_name')

import matplotlib.pyplot as plt

Months = [1,2,3,4]
Sales = [1000,2000,1500,1400]

plt.plot(Months,Sales, color='Pink',linestyle='--',linewidth = 2, marker='o', label='2025 Sales data')

plt.xlabel('Months')
plt.ylabel('Sales')
plt.legend()
plt.title("Monthly Sales Data")

plt.show()