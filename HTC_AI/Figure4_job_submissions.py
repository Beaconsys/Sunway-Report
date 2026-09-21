from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR
OUTPUT_DIR = Path.cwd()

plt.rcParams["font.family"] = "Arial"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams.update({
    "axes.labelsize": 45,
    "xtick.labelsize": 40,
    "ytick.labelsize": 40,
})


def load_matrix(machine):
    df = pd.read_csv(
        INPUT_DIR / f"{machine}_job_counts_1h.csv",
        parse_dates=["window_start"],
    )
    # Match the original blank-cell handling; do not alter any counts.
    df = df.loc[df["job_count"] > 0].copy()
    df["month"] = df["window_start"].dt.strftime("%Y-%m")
    df["day"] = df["window_start"].dt.day
    df["hour"] = df["window_start"].dt.hour
    cells = df.set_index(["month", "day", "hour"])["job_count"]
    # Hourly inputs must have a unique value per displayed cell.
    if not cells.index.is_unique:
        raise ValueError(f"Duplicate hourly cells in {machine} input")
    columns = pd.MultiIndex.from_product(
        [range(1, 32), range(24)], names=["day", "hour"]
    )
    return cells.unstack(["day", "hour"]).reindex(columns=columns, fill_value=0)


pivs = {machine: load_matrix(machine) for machine in ("TaihuLight", "OceanLight")}

vals = [p.values for p in pivs.values() if not p.empty]
all_vals = np.concatenate([v.ravel() for v in vals]) if vals else np.array([0.0])
vmin = float(np.nanmin(all_vals)) if all_vals.size else 0.0
vmax = float(np.nanmax(all_vals)) if all_vals.size else 10000

boundaries = [0, 200, 1000, 4000, 8000, 10000]
norm = BoundaryNorm(boundaries, ncolors=256)

row_counts = [len(p) for p in pivs.values() if not p.empty]
max_rows = max(row_counts) if row_counts else 1
fig_height = max(3.0, max_rows * 0.22 * 0.5 * 1.2 * 1.3)

fig1 = plt.figure(figsize=(12, fig_height), constrained_layout=True)
gs1 = fig1.add_gridspec(nrows=1, ncols=2, width_ratios=[1, 0.045])
ax_l1 = fig1.add_subplot(gs1[0, 0])
cax1 = fig1.add_subplot(gs1[0, 1])
cax1.axis('off')

piv = pivs["TaihuLight"]
if not piv.empty:
    im1 = ax_l1.imshow(piv.values, aspect='auto', norm=norm, cmap='Greys', interpolation='nearest')

    months = pd.Index(piv.index)
    if len(months) > 0:
        step = 6
        yticks = list(range(0, len(months), step))
        ylabels = [str(months[i]) for i in yticks]
        ax_l1.set_yticks(yticks)
        ax_l1.set_yticklabels(ylabels)
    else:
        ax_l1.set_yticks([])

    n_days = 31
    n_hours = n_days * 24
    xticks = np.linspace(0, n_hours - 1, 5, dtype=int)
    xtick_labels = [str(h) for h in xticks]

    ax_l1.set_xticks(xticks)
    ax_l1.set_xticklabels(xtick_labels, rotation=0)
    ax_l1.set_xlabel("Time (Hour)", fontweight='bold')
    ax_l1.set_ylabel("Time (YYYY-MM)", fontweight='bold')

fig2 = plt.figure(figsize=(13.5, fig_height), constrained_layout=True)
gs2 = fig2.add_gridspec(nrows=1, ncols=3, width_ratios=[1, 0.045, 0.05])
ax_l2 = fig2.add_subplot(gs2[0, 0])
cax2 = fig2.add_subplot(gs2[0, 2])

piv = pivs["OceanLight"]
if not piv.empty:
    im2 = ax_l2.imshow(piv.values, aspect='auto', norm=norm, cmap='Greys', interpolation='nearest')

    months = pd.Index(piv.index)
    if len(months) > 0:
        step = 6
        yticks = list(range(0, len(months), step))
        ylabels = [str(months[i]) for i in yticks]
        ax_l2.set_yticks(yticks)
        ax_l2.set_yticklabels(ylabels)
    else:
        ax_l2.set_yticks([])

    n_days = 31
    n_hours = n_days * 24
    xticks = np.linspace(0, n_hours - 1, 5, dtype=int)
    xtick_labels = [str(h) for h in xticks]

    ax_l2.set_xticks(xticks)
    ax_l2.set_xticklabels(xtick_labels, rotation=0)
    ax_l2.set_xlabel("Time (Hour)", fontweight='bold')
    ax_l2.set_ylabel("")

cb2 = fig2.colorbar(im2, cax=cax2)
cb2.ax.tick_params(labelsize=40)

fig1.savefig(OUTPUT_DIR / "Figure4a_TaihuLight_From_Counts.pdf", dpi=300)
fig2.savefig(OUTPUT_DIR / "Figure4b_OceanLight_From_Counts.pdf", dpi=300)


print(f"Saved figures to: {OUTPUT_DIR}")
plt.show()
plt.close("all")
