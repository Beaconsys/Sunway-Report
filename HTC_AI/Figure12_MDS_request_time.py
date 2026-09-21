from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter


plt.rcParams["font.family"] = "Arial"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

WAITING_TIME_PDF_FILE = Path.cwd() / "Figure12a_MDS_Request_Waiting_Time.pdf"
EXECUTION_TIME_PDF_FILE = Path.cwd() / "Figure12b_MDS_Request_Execution_Time.pdf"
TIME_INTERVALS = (
    "<0.010",
    "0.010-0.10",
    "0.10-1.0",
    "1.0-10",
    "10-100",
    "100-1000",
    ">=1000",
)

# Values transcribed from Figure 12. A height of 0.05 renders bars labeled <0.1.
WAIT_TAIHU_VALUES = (60.7, 1.1, 37.2, 1.1, 0.05, 0.05, 0.05)
WAIT_OCEAN_VALUES = (60.3, 22.6, 5.3, 8.3, 3.5, 0.05, 0.05)
WAIT_TAIHU_LABELS = ("60.7", "1.1", "37.2", "1.1", "<0.1", "<0.1", "<0.1")
WAIT_OCEAN_LABELS = ("60.3", "22.6", "5.3", "8.3", "3.5", "<0.1", "<0.1")

EXEC_TAIHU_VALUES = (19.7, 44.7, 9.2, 11.6, 12.9, 1.8, 0.05)
EXEC_OCEAN_VALUES = (28.5, 56.5, 5.3, 5.6, 3.6, 0.4, 0.05)
EXEC_TAIHU_LABELS = ("19.7", "44.7", "9.2", "11.6", "12.9", "1.8", "<0.1")
EXEC_OCEAN_LABELS = ("28.5", "56.5", "5.3", "5.6", "3.6", "0.4", "<0.1")


def add_value_labels(axis, bars, labels):
    for bar, label in zip(bars, labels):
        axis.annotate(
            label,
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=14,
        )


def draw_panel(axis, taihu_values, ocean_values, taihu_labels, ocean_labels):
    positions = np.arange(len(TIME_INTERVALS))
    width = 0.38
    taihu_bars = axis.bar(
        positions - width / 2,
        taihu_values,
        width,
        label="TaihuLight",
        color="#1f77b4",
        edgecolor="black",
    )
    ocean_bars = axis.bar(
        positions + width / 2,
        ocean_values,
        width,
        label="OceanLight",
        color="#ff7f0e",
        edgecolor="black",
    )
    add_value_labels(axis, taihu_bars, taihu_labels)
    add_value_labels(axis, ocean_bars, ocean_labels)

    axis.set_ylim(0, 120)
    axis.set_ylabel("System time", fontsize=25, fontweight="bold")
    axis.set_xticks(positions, TIME_INTERVALS)
    axis.yaxis.set_major_formatter(PercentFormatter(xmax=100))
    axis.tick_params(axis="both", labelsize=20)
    axis.legend(loc="upper left", fontsize=20)
    axis.set_xlabel("Time interval (ms)", fontsize=25, fontweight="bold")


def create_figure(taihu_values, ocean_values, taihu_labels, ocean_labels):
    figure, axis = plt.subplots(figsize=(12, 7))
    draw_panel(
        axis,
        taihu_values,
        ocean_values,
        taihu_labels,
        ocean_labels,
    )
    figure.tight_layout()
    return figure


def main():
    waiting_time_figure = create_figure(
        WAIT_TAIHU_VALUES,
        WAIT_OCEAN_VALUES,
        WAIT_TAIHU_LABELS,
        WAIT_OCEAN_LABELS,
    )
    waiting_time_figure.axes[0].set_title("Request waiting time", fontsize=25, fontweight="bold")

    execution_time_figure = create_figure(
        EXEC_TAIHU_VALUES,
        EXEC_OCEAN_VALUES,
        EXEC_TAIHU_LABELS,
        EXEC_OCEAN_LABELS,
    )
    execution_time_figure.axes[0].set_title("Request execution time", fontsize=25, fontweight="bold")
    plt.show()
    waiting_time_figure.savefig(WAITING_TIME_PDF_FILE, format="pdf", bbox_inches="tight")
    execution_time_figure.savefig(EXECUTION_TIME_PDF_FILE, format="pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
