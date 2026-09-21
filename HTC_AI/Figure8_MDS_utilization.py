from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import ticker
import pandas as pd


DATA_FILE = Path(__file__).with_name("MDS_utilization.csv")
OUTPUT_FILE = Path.cwd() / "Figure8_MDS_Utilization.pdf"

plt.rcParams["font.family"] = "Arial"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

data = pd.read_csv(DATA_FILE)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    data["MDS_Utilization_Percent"],
    data["TaihuLight_System_Time_Percent"],
    label="TaihuLight",
    color="blue",
    linewidth=2,
)
ax.plot(
    data["MDS_Utilization_Percent"],
    data["OceanLight_System_Time_Percent"],
    label="OceanLight",
    color="red",
    linewidth=2,
)

ax.set_xlabel("MDS utilization", fontsize=25, fontweight="bold")
ax.set_ylabel("System time", fontsize=25, fontweight="bold")
ax.tick_params(axis="both", labelsize=20)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda value, _: f"{value:.0f}%"))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda value, _: f"{value:.0f}%"))
ax.legend(fontsize=20, loc="upper left")
ax.grid(False)

fig.tight_layout()
plt.show()
fig.savefig(OUTPUT_FILE, format="pdf")
