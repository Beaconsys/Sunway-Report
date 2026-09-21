import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter


plt.rcParams["font.family"] = "Arial"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
INPUT_CSV_FILE = SCRIPT_DIRECTORY / "Cache_hit_ratio_comparation.csv"
OUTPUT_PDF_FILE = SCRIPT_DIRECTORY / "Figure18_Cache_Hit_Ratio.pdf"


def load_plot_data():
    with INPUT_CSV_FILE.open(newline="", encoding="utf-8") as input_file:
        rows = list(csv.DictReader(input_file))
    applications = [row["application"] for row in rows]
    default = [float(row["default"]) for row in rows]
    domain_aware_scheduling = [float(row["domain_aware_scheduling"]) for row in rows]
    return applications, default, domain_aware_scheduling


def main():
    applications, default, domain_aware_scheduling = load_plot_data()
    positions = np.arange(len(applications))
    width = 0.35

    figure, axis = plt.subplots(figsize=(12, 7))
    axis.bar(
        positions - width / 2,
        default,
        width,
        label="Default",
        color="#1f77b4",
        edgecolor="black",
    )
    axis.bar(
        positions + width / 2,
        domain_aware_scheduling,
        width,
        label="Domain-aware scheduling",
        color="#ff7f0e",
        edgecolor="black",
    )

    axis.set_ylabel("Cache hit ratio", fontsize=25, fontweight="bold")
    axis.set_xticks(positions, applications, fontweight="bold")
    axis.tick_params(axis="both", labelsize=20)
    axis.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    axis.legend(loc="upper left", fontsize=20)
    figure.tight_layout()
    plt.show()
    figure.savefig(OUTPUT_PDF_FILE, format="pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
