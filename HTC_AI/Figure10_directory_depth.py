from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

DATA_FILE = Path(__file__).with_name("Directory_depth.csv")
OUTPUT_FILE = Path.cwd() / "Figure10_Directory_Depth.pdf"

plt.rcParams["font.family"] = "Arial"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

data = pd.read_csv(DATA_FILE)
depth_labels = data["Directory_Depth"].astype(str)
taihu = data["TaihuLight_Proportion"] * 100
ocean = data["OceanLight_Proportion"] * 100

x = np.arange(len(depth_labels))
bar_width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))

bars1 = ax.bar(
    x - bar_width/2,
    taihu,
    width=bar_width,
    label='TaihuLight',
    color='#1f77b4',
    edgecolor='black'
)

bars2 = ax.bar(
    x + bar_width/2,
    ocean,
    width=bar_width,
    label='OceanLight',
    color='#ff7f0e',
    edgecolor='black'
)

ax.set_xlabel('Directory depths', fontsize=25, fontweight="bold")
ax.set_ylabel('Directory proportion', fontsize=25, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(depth_labels, fontsize=20)
ax.set_yscale('log')
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.1f}%'))
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)

ax.set_ylim(top=150)

ax.legend(fontsize=20, loc='upper left')
plt.tight_layout()
plt.show()
fig.savefig(OUTPUT_FILE, format="pdf")
