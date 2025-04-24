import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Arial'

all_points = pd.read_csv("data.csv")

ml_data = all_points[all_points['workload_type'] == 'AI']
hpc_data = all_points[all_points['workload_type'] == 'HPC']

print(f"AI data_sum: {len(ml_data)}")
print(f"HPC data_sum: {len(hpc_data)}")

plt.figure(figsize=(16, 9))

sns.scatterplot(data=ml_data, x='avg_mdops', y='total_iobw',
                color='#ff7f0e', alpha=1, label='AI Workloads',
                s=100, edgecolor='black', linewidth=1)
sns.scatterplot(data=hpc_data, x='avg_mdops', y='total_iobw',
                color='#1f77b4', alpha=1, label='HPC Workloads', 
                s=100, edgecolor='black', linewidth=1)

plt.xlabel('Average Metadata Operations (ops/s)', fontsize=35, fontweight='bold')
plt.ylabel('Total I/O Bandwidth (MB/s)', fontsize=35, fontweight='bold')

plt.xticks(fontsize=30)
plt.yticks(fontsize=30)

plt.ticklabel_format(style='sci', axis='both', scilimits=(0,0))

ax = plt.gca()
ax.xaxis.get_offset_text().set_fontsize(30)
ax.yaxis.get_offset_text().set_fontsize(30)

handles, labels = ax.get_legend_handles_labels()
plt.legend([handles[1], handles[0]], [labels[1], labels[0]], 
           fontsize=30, loc='best')

plt.tight_layout()

# 保存为PDF矢量图
plt.savefig("IO comparsion between HPC and AI.pdf", format='pdf', bbox_inches='tight')
print(f"\n saved : 'IO comparsion between HPC and AI.pdf'")

plt.show()