from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import PercentFormatter


SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_FILE = SCRIPT_DIR / "File_access_proportions.csv"
OUTPUT_FILE = SCRIPT_DIR / "Figure17b_File_Access_Proportion.pdf"

plt.rcParams["font.family"] = "Arial"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42


def main():
    data = pd.read_csv(INPUT_FILE)
    positions = np.arange(len(data))
    bar_width = 0.35

    figure, axis = plt.subplots(figsize=(8, 6))
    axis.bar(
        positions - bar_width / 2,
        data["taihulight_percent"],
        width=bar_width,
        color="#1f77b4",
        edgecolor="black",
        linewidth=1.2,
        label="TaihuLight",
    )
    axis.bar(
        positions + bar_width / 2,
        data["oceanlight_percent"],
        width=bar_width,
        color="#ff7f0e",
        edgecolor="black",
        linewidth=1.2,
        label="OceanLight",
    )

    axis.set_ylim(0, 110)
    axis.set_yticks(np.arange(0, 100, 20))
    axis.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
    axis.set_xticks(positions)
    axis.set_xticklabels(data["file_count_range"], fontsize=20)
    axis.set_xlabel("Number of files", fontsize=25, fontweight="bold")
    axis.set_ylabel("Job's proportion", fontsize=25, fontweight="bold")
    axis.tick_params(axis="y", labelsize=20)
    axis.grid(False)

    for spine in axis.spines.values():
        spine.set_linewidth(1.2)

    legend = axis.legend(loc="upper left", fontsize=20, frameon=True)
    legend.get_frame().set_linewidth(1.0)

    figure.tight_layout()
    plt.show()
    figure.savefig(OUTPUT_FILE, format="pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
