from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = SCRIPT_DIR / "Figure22_Write_Read_Bandwidth.pdf"

plt.rcParams["font.family"] = "Arial"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

BLUE = "#1f77b4"
ORANGE = "#ff7f0e"
BLUE_GRADIENT = LinearSegmentedColormap.from_list(
    "blue_gradient", ["#d6e8f4", BLUE]
)
ORANGE_GRADIENT = LinearSegmentedColormap.from_list(
    "orange_gradient", ["#fee0c2", ORANGE]
)


def load_column(filename, column):
    data = pd.read_csv(SCRIPT_DIR / filename)
    return data[column].to_numpy()


def add_density_gradient(axis, body, colormap):
    vertices = body.get_paths()[0].vertices
    y_values = np.unique(vertices[:, 1])
    left = np.empty_like(y_values)
    right = np.empty_like(y_values)

    for index, value in enumerate(y_values):
        x_values = vertices[np.isclose(vertices[:, 1], value), 0]
        left[index] = x_values.min()
        right[index] = x_values.max()

    widths = right - left
    maximum_width = widths.max()
    for index in range(len(y_values) - 1):
        intensity = (widths[index] + widths[index + 1]) / (2 * maximum_width)
        axis.fill_betweenx(
            y_values[index : index + 2],
            left[index : index + 2],
            right[index : index + 2],
            color=colormap(intensity),
            linewidth=0,
            zorder=1,
        )


def main():
    datasets = [
        load_column("GRIST_write.csv", "io_bandwidth_mb_s"),
        load_column("GRIST_read.csv", "io_bandwidth_mb_s"),
        load_column("CWRF_write.csv", "io_bandwidth_mb_s"),
        load_column("CWRF_read.csv", "io_bandwidth_mb_s"),
    ]
    colormaps = [BLUE_GRADIENT, ORANGE_GRADIENT, BLUE_GRADIENT, ORANGE_GRADIENT]

    figure, axis = plt.subplots(figsize=(12, 7))
    violin = axis.violinplot(
        datasets,
        showmeans=False,
        showmedians=True,
        showextrema=False,
        widths=0.8,
        points=100,
    )

    for body, colormap in zip(violin["bodies"], colormaps):
        add_density_gradient(axis, body, colormap)
        body.set_facecolor("none")
        body.set_edgecolor("black")
        body.set_linewidth(1.5)
        body.set_alpha(1)
        body.set_zorder(2)

    violin["cmedians"].set_color("black")
    violin["cmedians"].set_linewidth(1.5)

    axis.set_xlim(0.4, 4.6)
    axis.set_ylim(0, 1200)
    axis.set_yticks(np.arange(0, 1200, 200))
    axis.set_xticks([1, 2, 3, 4])
    axis.set_xticklabels(["GRIST", "GRIST", "CWRF", "CWRF"], fontsize=20, fontweight="bold")
    axis.set_ylabel("I/O bandwidth (MB/s)", fontsize=25, fontweight="bold")
    axis.tick_params(axis="y", labelsize=20)
    axis.grid(False)

    for spine in axis.spines.values():
        spine.set_linewidth(1.75)
        spine.set_edgecolor("black")

    legend = axis.legend(
        handles=[
            Patch(facecolor=BLUE, edgecolor="black", label="Write"),
            Patch(facecolor=ORANGE, edgecolor="black", label="Read"),
        ],
        loc="upper left",
        fontsize=20,
        frameon=True,
    )
    legend.get_frame().set_edgecolor("black")
    legend.get_frame().set_linewidth(1.75)

    figure.tight_layout()
    plt.show()
    figure.savefig(OUTPUT_FILE, format="pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
