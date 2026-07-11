# plt.bar(x,height, color='Color_name',width=value,label='label_name')

import matplotlib.pyplot as plt

product = ['A','B','C','D']
Sales = [1000,1500,800,1200]
plt.bar(product,Sales, color='red',width=0.1,label='Sales 2025')
plt.xlabel('product')
plt.ylabel('Sales')
plt.title('Product Sales comparison')
plt.legend()
plt.show()