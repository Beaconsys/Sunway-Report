from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_FILE = SCRIPT_DIR / "Hada_RPC_data.csv"
OUTPUT_FILE = SCRIPT_DIR / "Figure21_HadaFS_Migration.pdf"

plt.rcParams["font.family"] = "Arial"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42


def main():
    data = pd.read_csv(INPUT_FILE)

    figure, read_axis = plt.subplots(figsize=(12, 7))
    write_axis = read_axis.twinx()

    read_line, = read_axis.plot(
        data["minutes"],
        data["read_gb"],
        color="blue",
        linewidth=1.5,
        label="CN read",
    )
    write_line, = write_axis.plot(
        data["minutes"],
        data["write_gb"],
        color="red",
        linewidth=1.5,
        label="FWD write",
    )

    read_axis.set_xlim(0, data["minutes"].max())
    read_axis.set_ylim(0, 20)
    write_axis.set_ylim(0, 1.8)
    read_axis.set_yticks(range(0, 21, 5))
    write_axis.set_yticks([value / 4 for value in range(0, 8)])
    read_axis.set_xlabel("Time (Minute)", fontsize=25, fontweight="bold", labelpad=15)
    read_axis.set_ylabel(
        "CN read bandwidth (GB/s)", fontsize=25, fontweight="bold", labelpad=15
    )
    write_axis.set_ylabel(
        "FWD write bandwidth (GB/s)", fontsize=25, fontweight="bold", labelpad=15
    )
    read_axis.tick_params(axis="both", labelsize=20)
    write_axis.tick_params(axis="y", labelsize=20)
    read_axis.grid(False)
    write_axis.grid(False)

    for axis in (read_axis, write_axis):
        for spine in axis.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(2)
            spine.set_edgecolor("black")

    read_axis.legend(
        [read_line, write_line],
        [read_line.get_label(), write_line.get_label()],
        loc="upper right",
        fontsize=20,
        frameon=True,
    )

    figure.tight_layout()
    plt.show()
    figure.savefig(OUTPUT_FILE, format="pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
