import matplotlib.pyplot as plt
import numpy as np


categories = ['Fluid Dynamics', 'Metarials Chemistry', 'Earth Sciences', 'Artificial Intelligence', 'Others']

categories_multiline = ['Fluid\nDynamics', 'Materials\nChemistry', 'Earth\nSciences', 'Artificial\nIntelligence', 'Others']

OceanLight = [7.7, 20.8, 55.4, 3.9, 15.2]
TaihuLight = [6.1, 14.1, 71.2, 0.5, 8.1]

plt.rcParams['font.family'] = 'Arial'
plt.figure(figsize=(16, 9))

x = np.arange(len(categories))
width = 0.4

rects1 = plt.bar(x + width/2, OceanLight, width, label='OceanLight', color='#ff7f0e', edgecolor='black', linewidth=1.5)
rects2 = plt.bar(x - width/2, TaihuLight, width, label='TaihuLight', color='#1f77b4', edgecolor='black', linewidth=1.5)

title = 'Application Distribution Comparison'

# plt.xlabel('Class')
plt.ylabel('Application Distribution (%)', fontsize=35, fontweight='bold')
# plt.title(title)
plt.xticks(x, categories_multiline, rotation=0, fontsize=30)
plt.yticks(fontsize=30)

handles, labels = plt.gca().get_legend_handles_labels()
plt.legend([handles[1], handles[0]], [labels[1], labels[0]], fontsize=30)

plt.tight_layout()

plt.savefig(f"{title}.pdf", format='pdf', bbox_inches='tight')
print(f"saved : {title}.pdf")

plt.show()

