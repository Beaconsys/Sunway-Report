import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path



OUTPUT_FILE = Path(__file__).resolve().parent / "Figure23_Read_Bandwidth_Scaling.pdf"

MODE_LABELS = [
    "Mode 1",
    "Mode 2",
    "Mode 3",
    "Mode 4"
]

COLORS = [
    "#ff7f0e",   # Case 2
    "#f1af75",   # Case 1
    "#5286ab",   # Case 3
    "#1753ac"    # Case 4
]

BAR_WIDTH = 0.15

############################################################
# DATA
############################################################

processes = [1, 2, 4, 8, 16]

mode2 = [31.32, 45.62, 57.71, 74.36, 85.12]
mode1 = [5.57, 11.26, 20.15, 23.45, 39.51]
mode3 = [81.25, 117.49, 161.28, 272.81, 399.45]
mode4 = [73.15, 115.27, 173.45, 281.84, 408.15]



plt.rcParams.update({
    "font.family": "Arial",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})



x = np.arange(len(processes))

fig, ax = plt.subplots(figsize=(12, 5))

ax.bar(x - 1.5 * BAR_WIDTH, mode1,
       width=BAR_WIDTH,
       color=COLORS[0],
       edgecolor="black",
       linewidth=1.2,
       label=MODE_LABELS[0])

ax.bar(x - 0.5 * BAR_WIDTH, mode2,
       width=BAR_WIDTH,
       color=COLORS[1],
       edgecolor="black",
       linewidth=1.2,
       label=MODE_LABELS[1])

ax.bar(x + 0.5 * BAR_WIDTH, mode3,
       width=BAR_WIDTH,
       color=COLORS[2],
       edgecolor="black",
       linewidth=1.2,
       label=MODE_LABELS[2])

ax.bar(x + 1.5 * BAR_WIDTH, mode4,
       width=BAR_WIDTH,
       color=COLORS[3],
       edgecolor="black",
       linewidth=1.2,
       label=MODE_LABELS[3])



ax.set_xticks(x)
ax.set_xticklabels(processes, fontsize=20)
ax.set_xlabel("Number of processes", fontsize=25, fontweight='bold')

ax.set_ylabel("Read bandwidth (MB/s)", fontsize=25, fontweight='bold')
ax.tick_params(axis='y', labelsize=20)

ax.grid(False)

for spine in ax.spines.values():
    spine.set_linewidth(1.2)

legend = ax.legend(
    fontsize=18,
    frameon=True
)

legend.get_frame().set_linewidth(1.0)



plt.tight_layout()

plt.show()

plt.savefig(
    OUTPUT_FILE,
    format="pdf",
    bbox_inches="tight"
)
