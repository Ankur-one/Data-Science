# plt.plot(x,y color='color_name',Linestyle='Line_style', Linewidth=value,marker='marker symbol',label='label_name')

import matplotlib.pyplot as plt

Months = [1,2,3,4]
Sales = [1000,1200,800,1400]

plt.plot(Months,Sales, color='blue',linestyle='--',linewidth=2,marker='o',label='2025 Sales Data')

plt.xlabel('Months')
plt.ylabel('Sales per month')
plt.title("Monthly Sales Data report")
plt.legend(loc='upper left',fontsize=12)
plt.grid(color='Gray',linestyle=':',linewidth=1)
plt.show()