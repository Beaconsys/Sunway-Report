import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

plt.rcParams['font.family'] = 'Arial'

merged_data = pd.read_csv("Cache hit data.csv")

if 'Time' in merged_data.columns:
    merged_data['Time'] = pd.to_datetime(merged_data['Time'])

FONT_SIZE_AXIS_LABEL = 25
FONT_SIZE_TICKS = 20
FONT_SIZE_LEGEND = 22

fig, axs = plt.subplots(2, 1, figsize=(16, 9), sharex=True, 
                        gridspec_kw={'height_ratios': [1, 1], 'hspace': 0.08})

time_labels = []
if len(merged_data) > 0:
    num_labels = 5
    indices = np.linspace(0, len(merged_data)-1, num_labels, dtype=int)
    selected_times = merged_data['Time'].iloc[indices]
    time_labels = [pd.to_datetime(t).strftime('%Y-%m-%d') for t in selected_times]

ax1 = axs[0]
line1 = ax1.plot(np.arange(len(merged_data)), merged_data['read_sum_norm'], color='green', alpha=0.9, lw=2.5, label='FWD Burst Volume')
line2 = ax1.plot(np.arange(len(merged_data)), merged_data['burst_avg_io_rate_norm'], color='red', alpha=0.9, lw=2.5, label='OST Burst Volume')
ax1.set_ylabel('Normalized Volume', fontsize=FONT_SIZE_AXIS_LABEL, fontweight='bold')
ax1.set_yscale('log')
ax1.set_ylim(0.01, 1.1)
ax1.yaxis.set_major_formatter(ticker.ScalarFormatter())
ax1.tick_params(axis='y', labelsize=FONT_SIZE_TICKS)

ax1.spines['bottom'].set_visible(True)
ax1.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
ax1.grid(False)
ax1.legend(fontsize=FONT_SIZE_LEGEND, loc='lower right', framealpha=1, bbox_to_anchor=(0.995, 0.0))
for spine in ax1.spines.values():
    spine.set_linewidth(1.5)

ax2 = axs[1]
line3 = ax2.plot(np.arange(len(merged_data)), merged_data['hit_ratio_avg'], color='blue', alpha=0.9, lw=2.5, label='   Cache Hit Rate   ')
ax2.set_ylabel('Hit Rate(%)', fontsize=FONT_SIZE_AXIS_LABEL, fontweight='bold', labelpad=22)
ax2.set_xlabel('Date', fontsize=FONT_SIZE_AXIS_LABEL, fontweight='bold')
ax2.set_ylim(0, 80)
ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))
ax2.tick_params(axis='y', labelsize=FONT_SIZE_TICKS)

ax2.spines['top'].set_visible(True)
ax2.grid(False)

ax2.legend(fontsize=FONT_SIZE_LEGEND, loc='upper right', framealpha=1, bbox_to_anchor=(0.995, 1))
for spine in ax2.spines.values():
    spine.set_linewidth(1.5)

if len(merged_data) > 0:
    ax2.set_xticks(indices)
    ax2.set_xticklabels(time_labels, rotation=0)
    ax2.tick_params(axis='x', labelsize=FONT_SIZE_TICKS, pad=10)

for ax in axs:
    ax.set_xlim(-1, len(merged_data))

lines = line1 + line2 + line3
labels = [l.get_label() for l in lines]

plt.tight_layout(rect=[0.12, 0, 1, 1])  # [left, bottom, right, top]

filename = "Cache Hit Rate and Read Burst.pdf"
plt.savefig(filename, format='pdf', bbox_inches='tight')
print(f"saved : {filename}")
plt.show()