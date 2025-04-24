import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['xtick.labelsize'] = 30
plt.rcParams['ytick.labelsize'] = 30
plt.rcParams['legend.fontsize'] = 30

csv_file = 'mds utilization.csv'
df = pd.read_csv(csv_file)

x_table = df['x_table']
ocean = df['OceanLight']
taihu = df['TaihuLight']

plt.figure(figsize=(16, 9))

plt.plot(x_table, taihu, label='TaihuLight', color='blue', linewidth=2)
plt.plot(x_table, ocean, label='OceanLight', color='red', linewidth=2)

plt.xlabel('CDF of % Peak MDS Utilization (%)', fontsize=35, fontweight='bold')
plt.ylabel('System Time (%)', fontsize=35, fontweight='bold')

plt.legend()

plt.grid(False)

plt.tight_layout()
plt.show()
