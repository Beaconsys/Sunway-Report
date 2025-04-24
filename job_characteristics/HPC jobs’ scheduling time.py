import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

fixed_normal_values = [1.138, 1.332, 4.346, 7.952, 20.284, 30.642]
fixed_abnormal_values = [3.272, 7.332, 9.657, 12.367, 25.024, 34.112]
results_df = [r"$(10^0, 10^1]$", r"$(10^1, 10^2]$", r"$(10^2, 10^3]$",
              r"$(10^3, 10^4]$", r"$(10^4, 10^5]$", r"$(10^5, 10^6)$"]   # 节点分组标签
scientific_labels = results_df

fixed_df = pd.DataFrame({
    'node': results_df,
    'Normal': fixed_normal_values,
    'Abnormal': fixed_abnormal_values
})

plt.rcParams['font.family'] = 'Arial'
plt.figure(figsize=(16, 9))

bar_width = 0.4
x = np.arange(len(fixed_df))

rects1 = plt.bar(x - bar_width/2, fixed_df['Normal'], bar_width, 
                 label='Job With Interference   ', color='#1f77b4', edgecolor='black', linewidth=1.5)
rects2 = plt.bar(x + bar_width/2, fixed_df['Abnormal'], bar_width, 
                 label='Job Without Interference', color='#ff7f0e', edgecolor='black', linewidth=1.5)

plt.xlabel('Job\'s Parallelism', fontsize=35, fontweight='bold')
plt.ylabel('Scheduling Time (Seconds)', fontsize=35, fontweight='bold')

plt.xticks(x, scientific_labels, rotation=0, fontsize=30)
plt.yticks(fontsize=30)

plt.legend(fontsize=30, loc='upper left')

plt.tight_layout()

plt.savefig('HTC_job_interference.pdf', format='pdf', bbox_inches='tight')

plt.show()