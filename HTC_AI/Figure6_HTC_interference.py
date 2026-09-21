import matplotlib.pyplot as plt
import numpy as np

# Data
labels = [
    r"$(10^{0},10^{1}]$",
    r"$(10^{1},10^{2}]$",
    r"$(10^{2},10^{3}]$",
    r"$(10^{3},10^{4}]$",
    r"$(10^{4},10^{5}]$",
    r"$(10^{5},10^{6}]$"
]
no_interference = np.array([1, 1, 4, 8, 21, 30], dtype=float)
with_interference = np.array([3, 7.5, 9.5, 12, 25, 33], dtype=float)

x = np.arange(len(labels))
width = 0.36

# Global styling
plt.rcParams["font.family"] = "Arial"
plt.rcParams["axes.labelweight"] = "bold"

fig, ax = plt.subplots(figsize=(12, 6))

# Bars with black stroke
ax.bar(x - width/2, no_interference, width,
       label="Job without interference",
       color="#1f77b4", edgecolor="black", linewidth=1.2)
ax.bar(x + width/2, with_interference, width,
       label="Job with interference",
       color="#ff7f0e", edgecolor="black", linewidth=1.2)

# Axes labels
ax.set_xlabel("Job's parallelism", fontsize=25, fontweight="bold")
ax.set_ylabel("Scheduling time (Seconds)", fontsize=25, fontweight="bold")

# Ticks
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=20)
ax.set_yticks(np.arange(0, 36, 5))
ax.set_ylim(0, 35)
ax.tick_params(axis="y", labelsize=20)

# Legend
ax.legend(loc="upper left", fontsize=20)

plt.tight_layout()
fig.savefig("Figure6_HPC_Interference.pdf", format="pdf", bbox_inches="tight")
plt.show()
