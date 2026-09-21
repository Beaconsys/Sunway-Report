import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter

# Data
apps = [
    "LAMMPS\n(153600)",
    "AWP\n(3840)",
    "Kmeans\n(4096)",
    "SWLBM\n(512)"
]

taihulight = [28, 3.8, 0.14, 1.7]
oceanlight = [91, 19, 16, 3.9]

# Global font
plt.rcParams["font.family"] = "Arial"

x = np.arange(len(apps))
width = 0.35

fig, ax = plt.subplots(figsize=(7, 6))

# TaihuLight
ax.bar(
    x - width / 2,
    taihulight,
    width,
    label="TaihuLight",
    color="#1f77b4",
    edgecolor="black",
    linewidth=1.5
)

# OceanLight
ax.bar(
    x + width / 2,
    oceanlight,
    width,
    label="OceanLight",
    color="#ff7f0e",
    edgecolor="black",
    linewidth=1.5
)

# Logarithmic scale
ax.set_yscale("log")

# Y-axis limits
ax.set_ylim(0.01, 1100)

# Custom y-axis ticks
# Display the tick at 0.01 as 0
yticks = [0.01, 0.1, 1, 10, 100]

ax.yaxis.set_major_locator(
    FixedLocator(yticks)
)

ax.yaxis.set_major_formatter(
    FixedFormatter(
        ["0", "0.1", "1", "10", "100"]
    )
)

# Y-axis label
ax.set_ylabel(
    "I/O bandwidth (GB/s)",
    fontsize=25,
    fontweight="bold"
)

# Hide the x-axis label
ax.set_xlabel("")

# X-axis ticks
ax.set_xticks(x)
ax.set_xticklabels(
    apps,
    fontsize=24,
    fontweight="bold"
)

# Y-axis tick font size
ax.tick_params(
    axis="y",
    labelsize=20
)

# Disable the background grid
ax.grid(False)

# Legend
legend = ax.legend(
    loc="upper left",
    fontsize=20,
    frameon=True,
    edgecolor="black",
    fancybox=False,
    framealpha=1.0
)

# Legend border width
legend.get_frame().set_linewidth(1.5)

# Axis border width
for spine in ax.spines.values():
    spine.set_linewidth(1.5)

plt.tight_layout()

plt.savefig(
    "average_io_bandwidth_log_bar.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
