import matplotlib.pyplot as plt

FONT_SIZE_LABEL = 25
FONT_SIZE_TEXT = 25

plt.rcParams['font.family'] = 'Arial'

labels = ['CoV >= Baseline\n(high load)', 'CoV >= Baseline\n(idle)', 'CoV < Baseline']
sizes = [0.6, 17.2, 82.2]
colors = ['#ff7f0e', '#62a5d1', '#1f77b4']

plt.figure(figsize=(9, 9))

wedges, texts = plt.pie(sizes,
                      colors=colors,
                      startangle=90,
                      wedgeprops={'edgecolor': 'black', 'linewidth': 1.5},  # 边框粗细1.5
                      autopct=None)

plt.annotate('0.6%',
            xy=(0, 0.4),
            xytext=(0, 1.05),
            ha='center',
            va='center',
            fontsize=FONT_SIZE_TEXT,
            fontweight='bold')

plt.annotate('17.2%',
            xy=(-0.46, 0.35),
            ha='center',
            va='center',
            fontsize=FONT_SIZE_TEXT,
            fontweight='bold')

plt.annotate('82.2%',
            xy=(0.2, -0.47),
            ha='center',
            va='center',
            fontsize=FONT_SIZE_TEXT,
            fontweight='bold')

plt.annotate(labels[0],
            xy=(0, 1),
            xytext=(0, 1.12),
            ha='center',
            va='bottom',
            fontsize=FONT_SIZE_TEXT)

plt.annotate(labels[1],
            xy=(-0.4, 0.5),
            xytext=(-0.46, 0.55),
            ha='center',
            va='center',
            fontsize=FONT_SIZE_TEXT)

plt.annotate(labels[2],
            xy=(0.2, -0.3),
            ha='center',
            va='center',
            fontsize=FONT_SIZE_TEXT)

plt.axis('equal')

filename = "CoV_FWD.pdf"
plt.savefig(filename, format='pdf', bbox_inches='tight')
print(f"saved : {filename}")

# 显示图表
plt.show()