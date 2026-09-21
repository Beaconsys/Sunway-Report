from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np


OUTPUT_FILE = Path.cwd() / "Figure11_Performance_Degradation.pdf"

plt.rcParams["font.family"] = "Arial"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

bins = ["0-40%", "40-60%", "60-80%", "80-100%"]
taihu = np.array([37.18, 29.54, 19.68, 13.60])
ocean = np.array([49.86, 28.13, 14.21, 7.80])

x = np.arange(len(bins))
width = 0.38

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(
    x - width / 2,
    taihu,
    width,
    label="TaihuLight",
    color="tab:blue",
    edgecolor="black",
    linewidth=1.2,
)
ax.bar(
    x + width / 2,
    ocean,
    width,
    label="OceanLight",
    color="tab:orange",
    edgecolor="black",
    linewidth=1.2,
)

ax.set_xticks(x, bins, fontsize=20)
ax.tick_params(axis="y", labelsize=20)
ax.set_xlabel("Performance degradation", fontsize=25, fontweight="bold")
ax.set_ylabel("Job's proportion", fontsize=25, fontweight="bold")
ax.set_ylim(0, 100)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda value, _: f"{value:.0f}%"))
ax.legend(fontsize=20, loc="upper left")

fig.tight_layout()
plt.show()
fig.savefig(OUTPUT_FILE, format="pdf")
