# plt.pie(values, label=label_list,color='color_list',autopct='%1.1f%%')

import matplotlib.pyplot as plt

Region = ['North', 'South', 'East', 'West']
Revenue = [3000, 2000, 1500, 1000]

# Pie chart
plt.pie(Revenue, labels=Region, colors=['orange', 'green', 'yellow', 'red'], autopct='%1.1f%%')

plt.title("Revenue Contribution by Region")
plt.show()
