from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import to_rgb
from matplotlib.patches import Polygon

BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR / "Batch_parallelism_counts.csv"
OUTPUT_PATH = Path.cwd() / "Figure5_Batch_Parallelism_Violin.pdf"
plt.rcParams["font.sans-serif"] = ["Arial"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams.update({"axes.labelsize": 25, "xtick.labelsize": 20, "ytick.labelsize": 20})
CUSTOM_XTICKS = ["Batch 1", "Batch 2", "Batch 3", "Batch 4"]
BW = 0.35

data = pd.read_csv(INPUT_PATH)
if data.empty or data[["parallelism", "job_count"]].isna().any().any():
    raise ValueError("Missing parallelism or sample counts")
for column in ("parallelism", "job_count"):
    if (data[column] <= 0).any() or (data[column] % 1 != 0).any():
        raise ValueError(f"{column} must contain positive integers")
if set(data["batch"]) != set(CUSTOM_XTICKS):
    raise ValueError("Expected Batch 1 through Batch 4")
group_data_for_violin = []
labels_drawn = []
for batch in CUSTOM_XTICKS:
    rows = data.loc[data["batch"] == batch]
    samples = np.repeat(rows["parallelism"].to_numpy(dtype=float),
                        rows["job_count"].to_numpy(dtype=int))
    if np.unique(samples).size < 2:
        raise ValueError(f"{batch} needs at least two distinct parallelism values")
    group_data_for_violin.append(samples)
    labels_drawn.append(batch)

def _blend_with_white(hex_color, t):
    r, g, b = to_rgb(hex_color)
    return (1 - (1 - r) * t, 1 - (1 - g) * t, 1 - (1 - b) * t)

def shade_violin_by_width(ax, body, base_color="#1f77b4", n_strips=240, gamma=1.05, draw_outline=True):
    path = body.get_paths()[0]
    verts = path.vertices
    ymin, ymax = np.min(verts[:, 1]), np.max(verts[:, 1])
    y_samples = np.linspace(ymin, ymax, n_strips + 1)

    xs_left, xs_right = [], []
    for y in y_samples:
        xs = []
        for (x1, y1), (x2, y2) in zip(verts[:-1], verts[1:]):
            if (y1 <= y <= y2) or (y2 <= y <= y1):
                if y2 != y1:
                    t = (y - y1) / (y2 - y1)
                    x = x1 + t * (x2 - x1)
                    xs.append(x)
        if len(xs) >= 2:
            xs.sort()
            xs_left.append(xs[0])
            xs_right.append(xs[-1])
        else:
            xs_left.append(np.nan)
            xs_right.append(np.nan)

    xs_left = np.array(xs_left)
    xs_right = np.array(xs_right)
    widths = xs_right - xs_left

    ok = np.isfinite(widths) & (widths > 0)
    if not np.any(ok):
        body.set_visible(True)
        return

    w = widths[ok]
    wmin, wmax = np.nanmin(w), np.nanmax(w)
    denom = (wmax - wmin) if (wmax - wmin) > 1e-12 else 1.0

    body.set_visible(False)

    for i in range(len(y_samples) - 1):
        if not ok[i] or not ok[i + 1]:
            continue
        y0, y1 = y_samples[i], y_samples[i + 1]
        xl0, xr0 = xs_left[i], xs_right[i]
        xl1, xr1 = xs_left[i + 1], xs_right[i + 1]
        w_avg = ((xr0 - xl0) + (xr1 - xl1)) * 0.5
        t = ((w_avg - wmin) / denom) ** gamma
        face = _blend_with_white(base_color, t)
        ax.fill_betweenx([y0, y1], [xl0, xl1], [xr0, xr1],
                         facecolor=face, edgecolor='none', zorder=body.get_zorder())

    if draw_outline:
        ax.add_patch(Polygon(verts, fill=False, edgecolor='black', linewidth=1.5, zorder=body.get_zorder()+0.5))


fig, ax = plt.subplots(figsize=(12, 6))
if group_data_for_violin:
    parts = ax.violinplot(
        dataset=group_data_for_violin,
        positions=np.arange(1, len(group_data_for_violin) + 1),
        widths=0.85,
        showmeans=False,
        showmedians=True,
        showextrema=False,
        bw_method=BW
    )

    for body in parts['bodies']:
        shade_violin_by_width(ax, body, base_color="#1f77b4", n_strips=260, gamma=1.1, draw_outline=True)

    if 'cmedians' in parts:
        parts['cmedians'].set_color('black')
        parts['cmedians'].set_linewidth(2)
        parts['cmedians'].set_zorder(999)

    ax.set_yscale('log')
    tick_candidates = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    all_vals = np.concatenate(group_data_for_violin)
    ymin, ymax = np.nanmin(all_vals), np.nanmax(all_vals)
    yticks = [t for t in tick_candidates if t >= max(1, ymin) and t <= max(ymax, 1)]
    if yticks:
        ax.set_yticks(yticks)
        ax.set_yticklabels([str(int(t)) for t in yticks])

    ax.set_xticks(np.arange(1, len(labels_drawn) + 1))
    custom = CUSTOM_XTICKS[:len(labels_drawn)] if isinstance(CUSTOM_XTICKS, (list, tuple)) else labels_drawn
    if len(custom) < len(labels_drawn):
        custom += labels_drawn[len(custom):]
    xtl = ax.set_xticklabels(custom, rotation=0)

    plt.setp(xtl, fontsize=25, fontweight='bold')
    ax.set_xlabel('')
    ax.set_ylabel('Parallelism', fontsize=25, fontweight='bold')
    plt.tight_layout()
    plt.show()
    fig.savefig(OUTPUT_PATH, dpi=300)
    print(f"Saved: {OUTPUT_PATH}")
else:
    raise ValueError("No batch data available")
