# plt.scatter(x,y color='color_name',marker='marker_style',label='label_name')

import matplotlib.pyplot as plt

hours_studies = [1,2,3,4,5,6,7,8]
exam_score = [25,35,45,55,65,75,85,95]

plt.scatter(hours_studies,exam_score, color='green',marker='o',label='Student Data')

plt.xlabel("Number of hours")
plt.ylabel("Exam Score")
plt.legend(loc='upper left')
plt.title("Relatonship between study time and exam score")
plt.grid(True)
plt.show()