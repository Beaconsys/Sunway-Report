import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Arial'

export_data = pd.read_csv("IO_interference_data.csv")

categories = export_data['category'].tolist()
normal_values = export_data['normal_ratio'].tolist()
abnormal_values = export_data['abnormal_ratio'].tolist()

FONT_SIZE_AXIS_LABEL = 35
FONT_SIZE_TICKS = 30
FONT_SIZE_LEGEND = 30

plt.figure(figsize=(16, 9))

x = np.arange(len(categories))
width = 0.5

normal_color = '#1f77b4'
abnormal_color = '#ff7f0e'

normal_bars = plt.bar(x, normal_values, width, label='Normal Job', 
                     color=normal_color, edgecolor='black', linewidth=1.5)

abnormal_bars = plt.bar(x, abnormal_values, width, bottom=normal_values, 
                       label='Abnormal Job', color=abnormal_color, 
                       edgecolor='black', linewidth=1.5)

plt.ylabel('Proportion', fontsize=FONT_SIZE_AXIS_LABEL, fontweight='bold')

plt.xticks(x, ['OceanLight\nRead', 'TaihuLight\nRead', 'OceanLight\nWrite', 'TaihuLight\nWrite'], 
           fontsize=FONT_SIZE_TICKS)
plt.yticks(fontsize=FONT_SIZE_TICKS)

handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles, labels, fontsize=FONT_SIZE_LEGEND, loc='upper right')

plt.ylim(0, 1.35)
plt.grid(False)

filename = "IO_interference_Analysis.pdf"
plt.tight_layout()
plt.savefig(filename, format='pdf', bbox_inches='tight')
print(f"saved : {filename}")
plt.show()