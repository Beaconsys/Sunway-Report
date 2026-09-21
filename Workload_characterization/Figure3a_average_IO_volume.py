import numpy as np
import matplotlib.pyplot as plt

# Data units: MB
apps = ["LAMMPS\n(153600)", "AWP\n(3840)", "Kmeans\n(4096)", "SWLBM\n(512)"]

taihulight_mb = [
    215609.30,
    313764.95,
    154404.79,
    50943.95
]

oceanlight_mb = [
    263819.61,
    685789.12,
    1195971.66,
    82096.66
]

# MB -> GB
taihulight_gb = np.array(taihulight_mb) / 1024
oceanlight_gb = np.array(oceanlight_mb) / 1024

# Global font
plt.rcParams["font.family"] = "Arial"

x = np.arange(len(apps))
width = 0.35

fig, ax = plt.subplots(figsize=(7, 6))

# TaihuLight
ax.bar(
    x - width / 2,
    taihulight_gb,
    width,
    label="TaihuLight",
    color="#1f77b4",
    edgecolor="black",
    linewidth=1.5
)

# OceanLight
ax.bar(
    x + width / 2,
    oceanlight_gb,
    width,
    label="OceanLight",
    color="#ff7f0e",
    edgecolor="black",
    linewidth=1.5
)

# Y-axis label
ax.set_ylabel(
    "Average I/O volume (GB)",
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

# Y-axis ticks
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

# Axis borders
for spine in ax.spines.values():
    spine.set_linewidth(1.5)

plt.tight_layout()

plt.savefig(
    "average_io_volume_bar.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
