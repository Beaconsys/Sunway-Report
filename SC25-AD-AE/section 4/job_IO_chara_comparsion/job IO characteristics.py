import math

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

title = 'Job_IO_Chara_Comparison'
norm_stats_df = pd.read_csv(f'data.csv')

plot_data = []
positions = []
current_pos = 0.5

dimensions = norm_stats_df['dimension'].unique()

for dim in dimensions:
    dim_data = norm_stats_df[norm_stats_df['dimension'] == dim]

    new_data = dim_data[dim_data['group'] == 'New']

    new_q1 = new_data['q1_norm'].values[0]
    new_median = new_data['median_norm'].values[0]
    new_q3 = new_data['q3_norm'].values[0]
    new_min = new_data['min_norm'].values[0]
    new_max = new_data['max_norm'].values[0]

    n_points = 100
    new_synthetic_data = np.concatenate([
        np.linspace(new_min, new_q1, n_points//4),
        np.linspace(new_q1, new_median, n_points//4),
        np.linspace(new_median, new_q3, n_points//4),
        np.linspace(new_q3, new_max, n_points//4)
    ])

    for val in new_synthetic_data:
        plot_data.append({'dim': dim, 'group': 'New', 'value': val, 'pos': current_pos + 0.05})

    old_data = dim_data[dim_data['group'] == 'Old']
    old_q1 = old_data['q1_norm'].values[0]
    old_median = old_data['median_norm'].values[0]
    old_q3 = old_data['q3_norm'].values[0]
    old_min = old_data['min_norm'].values[0]
    old_max = old_data['max_norm'].values[0]

    old_synthetic_data = np.concatenate([
        np.linspace(old_min, old_q1, n_points//4),
        np.linspace(old_q1, old_median, n_points//4),
        np.linspace(old_median, old_q3, n_points//4),
        np.linspace(old_q3, old_max, n_points//4)
    ])

    for val in old_synthetic_data:
        plot_data.append({'dim': dim, 'group': 'Old', 'value': val, 'pos': current_pos - 0.05})
    
    positions.append(current_pos)
    current_pos += 2

df = pd.DataFrame(plot_data)

plt.figure(figsize=(16, 10))
ax = plt.gca()

sns.set_style("white")

plt.rcParams['font.family'] = 'Arial'

FONT_SIZE_AXIS_LABEL = 35
FONT_SIZE_TICKS = 30
FONT_SIZE_LEGEND = 30

plt.rcParams['patch.force_edgecolor'] = True

taihu_color = (255/255, 127/255, 14/255)  # #ff7f0e 橙色
ocean_color = (31/255, 119/255, 180/255)  # #1f77b4 蓝色

boxprops = {
    'linewidth': 1.5, 
    'edgecolor': 'black',
}

sns.boxplot(x='pos', y='value', hue='group', data=df,
            palette={'New': taihu_color, 'Old': ocean_color},  # 使用RGB元组代替十六进制
            width=0.5,
            fliersize=3, 
            linewidth=1,
            boxprops=boxprops, 
            whiskerprops={'linewidth': 1.5},
            medianprops={'color': 'black', 'linewidth': 2},
            showfliers=False,
            saturation=1.0  # 设置饱和度为100%，不降低颜色饱和度
            )

plt.ylabel('Normalized Value', fontsize=FONT_SIZE_AXIS_LABEL, fontweight='bold')
plt.ylim(-0.1, 1.2)
plt.xlabel('', fontsize=FONT_SIZE_AXIS_LABEL)

adjusted_positions = []
for i, pos in enumerate(positions):
    left_box_pos = pos - 0
    right_box_pos = pos + 0
    center_pos = (left_box_pos + right_box_pos) / 2
    adjusted_positions.append(center_pos)

x_labels = []
for dim in dimensions:
    if dim == 'read_operation_per_second':
        x_labels.append('Read Operation\nPer Second')
    elif dim == 'write_operation_per_second':
        x_labels.append('Write Operation\nPer Second')
    elif dim == 'meta_operation_per_second':
        x_labels.append('Meta Operation\nPer Second')
    else:
        x_labels.append(dim.replace('_', ' ').title())

plt.xticks(adjusted_positions, x_labels, 
           fontsize=FONT_SIZE_TICKS, 
           rotation=45,
           ha='right')

plt.yticks(fontsize=FONT_SIZE_TICKS)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, ['TaihuLight', 'OceanLight'],
          loc='upper right',
          frameon=True,
          shadow=True,
          edgecolor='white',
          fontsize=FONT_SIZE_LEGEND)

plt.savefig(f'{title}.pdf', format='pdf', bbox_inches='tight')
print(f"saved: {title}.pdf")
plt.show()