from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch


SCRIPT_DIR = Path(__file__).resolve().parent
TAIHU_FILE = SCRIPT_DIR / "TaihuLight_FWD_jobs.csv"
OCEAN_FILE = SCRIPT_DIR / "OceanLight_FWD_jobs.csv"
OUTPUT_FILE = SCRIPT_DIR / "Figure17a_Forwarding_Node_Jobs.pdf"

plt.rcParams["font.family"] = "Arial"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42


def load_data(filename, system_name):
    data = pd.read_csv(filename)
    data["system"] = system_name
    data["series"] = system_name + "_" + data["fwd_node"]
    return data


def main():
    taihu = load_data(TAIHU_FILE, "TaihuLight")
    ocean = load_data(OCEAN_FILE, "OceanLight")
    data = pd.concat([taihu, ocean], ignore_index=True)
    order = [
        "TaihuLight_FWD1",
        "TaihuLight_FWD2",
        "OceanLight_FWD1",
        "OceanLight_FWD2",
    ]
    palette = {
        "TaihuLight_FWD1": "#1f77b4",
        "TaihuLight_FWD2": "#1f77b4",
        "OceanLight_FWD1": "#ff7f0e",
        "OceanLight_FWD2": "#ff7f0e",
    }

    series_data = [
        data.loc[data["series"] == series, "job_number"].to_numpy()
        for series in order
    ]
    positions = [1, 2, 3, 4]

    figure, axis = plt.subplots(figsize=(12, 7))
    violin = axis.violinplot(
        series_data,
        positions=positions,
        showmeans=False,
        showmedians=False,
        showextrema=False,
        widths=0.65,
        points=100,
    )

    for body, series in zip(violin["bodies"], order):
        body.set_facecolor(palette[series])
        body.set_edgecolor("black")
        body.set_linewidth(1.5)
        body.set_alpha(0.8)

    for position, series in zip(positions, order):
        median = data.loc[data["series"] == series, "job_number"].median()
        line_length = 0.25 if series.startswith("OceanLight") else 0.1
        axis.hlines(
            median,
            position - line_length,
            position + line_length,
            colors="black",
            linewidth=2,
            zorder=3,
        )

    axis.set_ylim(0, 35)
    axis.set_xticks(positions)
    axis.set_xticklabels(["FWD1", "FWD2", "FWD1", "FWD2"], fontsize=20)
    axis.set_ylabel("Job number", fontsize=25, fontweight="bold")
    axis.tick_params(axis="y", labelsize=20)
    axis.grid(False)

    for spine in axis.spines.values():
        spine.set_linewidth(1.5)

    legend = axis.legend(
        handles=[
            Patch(facecolor="#1f77b4", edgecolor="black", label="TaihuLight"),
            Patch(facecolor="#ff7f0e", edgecolor="black", label="OceanLight"),
        ],
        loc="upper left",
        fontsize=20,
        frameon=True,
    )
    legend.get_frame().set_edgecolor("black")

    figure.tight_layout()
    plt.show()
    figure.savefig(OUTPUT_FILE, format="pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
