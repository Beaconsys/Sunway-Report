# plot_heatmap.py
import pickle
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 加载热力图数据
with open("heatmap_data.pkl", "rb") as f:
    heatmap_data = pickle.load(f)

GROUP_COUNT = heatmap_data.shape[0]

plt.rcParams.update({'font.size': 20, 'font.family': 'Arial'})

plt.figure(figsize=(10, 9))
ax = sns.heatmap(
    heatmap_data,
    cmap="Reds",
    xticklabels=[str(i) for i in range(24)],
    yticklabels=[f" {i + 1}" for i in range(GROUP_COUNT)],
    annot=False,
    cbar_kws={"ticks": [1, 2, 3, 4]}
)

cbar = ax.collections[0].colorbar
cbar.set_ticks([1, 2, 3, 4])
cbar.set_ticklabels(["0%", "33%", "66%", "100%"])

plt.xticks(rotation=0, fontsize=30)
plt.yticks(rotation=0, fontsize=30)
plt.xlabel("Time(hour)", fontsize=35, fontweight='bold')
plt.ylabel("Group id", fontsize=35, fontweight='bold')
plt.xticks(ticks=range(0, 28, 4), labels=[str(i) for i in range(0, 28, 4)], fontsize=30)
plt.gca().invert_yaxis()
cbar.ax.tick_params(labelsize=30)

plt.show()
