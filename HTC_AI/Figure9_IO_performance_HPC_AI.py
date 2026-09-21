from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = Path(__file__).with_name("HPC_AI_comparison.csv")
OUTPUT_FILE = Path.cwd() / "Figure9_IO_Performance_HPC_AI.pdf"

plt.rcParams["font.family"] = "Arial"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

all_points = pd.read_csv(DATA_FILE)

ml_data = all_points[all_points['workload_type'] == 'AI']
hpc_data = all_points[all_points['workload_type'] == 'HPC']


plt.figure(figsize=(16, 9))

plt.scatter(
    ml_data['avg_mdops'],
    ml_data['total_iobw'],
    color='#ff7f0e',
    alpha=1,
    label='AI Workloads',
    s=100,
    edgecolors='black',
    linewidths=1,
)
plt.scatter(
    hpc_data['avg_mdops'],
    hpc_data['total_iobw'],
    color='#1f77b4',
    alpha=1,
    label='HPC Workloads',
    s=100,
    edgecolors='black',
    linewidths=1,
)

plt.xlabel('Avg. metadata operations (Ops/s)', fontsize=35, fontweight='bold')
plt.ylabel('I/O bandwidth (MB/s)', fontsize=35, fontweight='bold')

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

plt.show()
plt.savefig(OUTPUT_FILE, format="pdf", bbox_inches="tight")
print(f"Saved: {OUTPUT_FILE}")
