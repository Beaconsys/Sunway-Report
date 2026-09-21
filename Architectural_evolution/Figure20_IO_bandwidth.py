from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch


plt.rcParams["font.family"] = "Arial"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

OUTPUT_PDF_FILE = Path(__file__).resolve().parent / "Figure20_IO_Bandwidth.pdf"

BOX_STATS_MBPS = {
    "TaihuLight Read": (434.99, 775.54, 1542.74, 200.05, 3199.88),
    "OceanLight GFS Read": (496.66, 1170.95, 3129.66, 200.28, 9995.26),
    "OceanLight HadaFS Read": (7956.92, 11220.51, 19018.55, 837.68, 22929.21),
    "TaihuLight Write": (494.27, 1213.21, 2031.96, 200.73, 4229.23),
    "OceanLight GFS Write": (417.75, 3490.46, 3938.46, 206.66, 10936.13),
    "OceanLight HadaFS Write": (13231.77, 14628.57, 20155.58, 960.00, 23162.91),
}
BOX_ORDER = (
    "TaihuLight Read",
    "OceanLight GFS Read",
    "OceanLight HadaFS Read",
    "TaihuLight Write",
    "OceanLight GFS Write",
    "OceanLight HadaFS Write",
)
POSITIONS = (1, 2, 3, 5, 6, 7)
COLORS = ("#1f77b4", "#ff7f0e", "darkgreen", "#1f77b4", "#ff7f0e", "darkgreen")


def make_box_statistics(label):
    lower_quartile, median, upper_quartile, lower_whisker, upper_whisker = BOX_STATS_MBPS[label]
    return {
        "med": median / 1024,
        "q1": lower_quartile / 1024,
        "q3": upper_quartile / 1024,
        "whislo": lower_whisker / 1024,
        "whishi": upper_whisker / 1024,
        "fliers": [],
    }


def main():
    figure, axis = plt.subplots(figsize=(12, 7))
    box_plot = axis.bxp(
        [make_box_statistics(label) for label in BOX_ORDER],
        positions=POSITIONS,
        showfliers=False,
        patch_artist=True,
        medianprops={"color": "black", "linewidth": 2},
        boxprops={"linewidth": 2},
        whiskerprops={"linewidth": 2},
        capprops={"linewidth": 2},
    )
    for box, color in zip(box_plot["boxes"], COLORS):
        box.set_facecolor(color)
        box.set_edgecolor("black")

    axis.set_ylabel("I/O bandwidth (GB/s)", fontsize=25, fontweight="bold")
    axis.set_xticks((1, 2, 3, 4, 5, 6, 7), ("", "Read bandwidth", "", "", "", "Write bandwidth", ""))
    axis.set_ylim(0, 32)
    axis.set_yticks(np.arange(0, 25, 4))
    axis.tick_params(axis="y", labelsize=20)
    for tick_label in axis.get_xticklabels():
        tick_label.set_fontsize(25)
        tick_label.set_fontweight("bold")
    for tick_line, tick_label in zip(axis.get_xticklines(), axis.get_xticklabels()):
        if not tick_label.get_text():
            tick_line.set_visible(False)

    axis.legend(
        handles=(
            Patch(facecolor="#1f77b4", edgecolor="black", label="TaihuLight"),
            Patch(facecolor="#ff7f0e", edgecolor="black", label="OceanLight(GFS)"),
            Patch(facecolor="darkgreen", edgecolor="black", label="OceanLight(HadaFS)"),
        ),
        loc="upper left",
        fontsize=20,
    )
    figure.tight_layout()
    plt.show()
    figure.savefig(OUTPUT_PDF_FILE, format="pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
