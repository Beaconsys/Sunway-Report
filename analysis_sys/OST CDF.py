import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Arial'

x = [0.5, 1, 5, 20, 50, 100]
taihu = [0, 61, 77, 99, 99.5, 100]
ocean = [0, 57, 84, 95, 98, 100]

plt.figure(figsize=(10, 9))

# 绘制折线图
plt.plot(x, taihu, label="TaihuLight", color='blue', linewidth=2)
plt.plot(x, ocean, label="OceanLight", color='red', linewidth=2)

plt.xscale('log')

xticks = [1, 5, 20, 50, 100]
xtick_labels = ['1%', '5%', '20%', '50%', '100%']
plt.xticks(xticks, xtick_labels, fontsize=30)
plt.yticks(fontsize=30)

plt.xlim(0.5, 100)
plt.ylim(0, 100)

plt.xlabel("CDF of % Peak OST Utilization", fontsize=35,fontweight='bold')
plt.ylabel("System Time(%)", fontsize=35,fontweight='bold')

plt.legend(loc = "upper left", fontsize=25)

plt.tight_layout()
plt.show()
