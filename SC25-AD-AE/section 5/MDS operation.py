import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

plt.rcParams['font.family'] = 'Arial'

categories = ["open", "close", "getattr", "statfs", "sync", "getxattr", "other"]
taihulight = [44, 43.8, 8.8, 0.27, 0.11, 0.39, 3.43]
oceanlight = [38.63, 38.63, 12.93, 4.06, 1.34, 1.33, 3.08]

x = np.arange(len(categories))
width = 0.35

plt.figure(figsize=(16, 9))

plt.bar(x - width/2, taihulight, width, label='TaihuLight', color='#1f77b4',
        edgecolor='black', linewidth=1.5)
plt.bar(x + width/2, oceanlight, width, label='OceanLight', color='#ff7f0e',
        edgecolor='black', linewidth=1.5)

plt.yscale('log')
ax = plt.gca()
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))

ticks = [0.1, 1, 10, 50, 100]
ax.set_yticks(ticks)

plt.ylabel('Operation number(%)', fontsize=35, fontweight='bold')
plt.xlabel('Metadata Operations', fontsize=35, fontweight='bold')
plt.xticks(x, categories, fontsize=30)
plt.yticks(fontsize=30)

plt.legend(fontsize=30)

plt.tight_layout()
plt.show()
