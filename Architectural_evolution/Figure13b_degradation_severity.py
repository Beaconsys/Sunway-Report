from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter


plt.rcParams["font.family"] = "Arial"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
DATA_FILES = (
    ("TaihuLight_read_degradation.csv", "TaihuLight read", "#1f77b4", "-"),
    ("OceanLight_read_degradation.csv", "OceanLight read", "red", "-"),
    ("TaihuLight_write_degradation.csv", "TaihuLight write", "#1f77b4", "--"),
    ("OceanLight_write_degradation.csv", "OceanLight write", "red", "--"),
)
OUTPUT_PDF_FILE = SCRIPT_DIRECTORY / "Figure13b_Degradation_Severity.pdf"


def load_degradation_values(filename):
    data = np.genfromtxt(SCRIPT_DIRECTORY / filename, delimiter=",", names=True)
    return np.sort(np.atleast_1d(data["degradation_percent"]))


def main():
    figure, axis = plt.subplots(figsize=(12, 7))
    for filename, label, color, linestyle in DATA_FILES:
        values = load_degradation_values(filename)
        cdf = np.arange(1, len(values) + 1) / len(values)
        axis.plot(values, cdf, label=label, color=color, linestyle=linestyle, linewidth=2)

    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.set_xlabel("Performance degradation", fontsize=25, fontweight="bold")
    axis.set_ylabel("Job's proportion", fontsize=25, fontweight="bold")
    axis.xaxis.set_major_formatter(PercentFormatter(xmax=1))
    axis.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    axis.tick_params(axis="both", labelsize=20)
    axis.legend(loc="upper left", fontsize=20)
    figure.tight_layout()
    plt.show()
    figure.savefig(OUTPUT_PDF_FILE, format="pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
