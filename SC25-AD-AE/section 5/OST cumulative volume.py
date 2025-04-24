import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "Arial"
plt.rcParams["axes.titlesize"] = 26
plt.rcParams["axes.labelsize"] = 26
plt.rcParams["xtick.labelsize"] = 20
plt.rcParams["ytick.labelsize"] = 20
plt.rcParams["legend.fontsize"] = 20

csv_file = "ost volume per minute.csv"
df = pd.read_csv(csv_file)

df["timestamp"] = pd.to_datetime(df["timestamp"])

df["cumulative_read_io"] = df["read_io"].cumsum() / (1024 * 1024)  # MB → TB
df["cumulative_write_io"] = df["write_io"].cumsum() / (1024 * 1024)  # MB → TB
df["cumulative_total_io"] = df["total_io"].cumsum() / (1024 * 1024)  # MB → TB

plt.rcParams["font.family"] = "Arial"

plt.figure(figsize=(10, 9))
plt.plot(df["timestamp"], df["cumulative_read_io"], label="Cumulative Read I/O", color="blue", linewidth=2)
plt.plot(df["timestamp"], df["cumulative_write_io"], label="Cumulative Write I/O", color="red", linewidth=2)
plt.plot(df["timestamp"], df["cumulative_total_io"], label="Cumulative Total I/O", color="green", linewidth=2)

plt.xlabel("Date", fontsize=35, fontweight='bold')
plt.ylabel("Cumulative I/O Volume (TB)", fontsize=35, fontweight='bold')  # 单位更新为 TB

timestamps = df["timestamp"]
tick_indices = np.linspace(0, len(timestamps) - 1, 3, dtype=int)
tick_labels = [timestamps[i].strftime("%Y-%m-%d") for i in tick_indices]
plt.xticks(ticks=timestamps.iloc[tick_indices], labels=tick_labels, fontsize=30, rotation=0)

plt.yticks(fontsize=30)

plt.legend(fontsize=25)

plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

ax = plt.gca()
ax.yaxis.get_offset_text().set_fontsize(30)

plt.tight_layout()
plt.show()
