import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline
from matplotlib.ticker import ScalarFormatter

plt.rcParams['font.family'] = 'Arial'

# OceanLight data
data = {
    "Day": list(range(1, 31)),
    "q_share": [429,123,71,290,213,86,85,80,660,413,391,300,356,359,491,174,107,319,452,421,45,89,289,453,246,340,433,262,69,360],
    "q_test": [10,13,15,3,5,10,0,9,13,13,5,13,0,8,0,9,7,12,5,14,1,11,14,0,11,4,12,5,14,2],
    "q_exec": [19,1,10,6,8,22,25,12,3,16,25,21,9,20,9,21,14,15,2,16,10,3,3,24,15,22,21,16,6,2]
}
df = pd.DataFrame(data)

df["q_test"] = df["q_test"].replace(0, 0.1)

plt.figure(figsize=(16, 9))

x = np.array(df["Day"])
x_smooth = np.linspace(x.min(), x.max(), 300)

def smooth_line(y_vals):
    y = np.array(y_vals)
    spline = make_interp_spline(x, y, k=3)  # 三次样条插值
    return spline(x_smooth)

plt.plot(x_smooth, smooth_line(df["q_share"]), label="q_share", linewidth=2, color='red')
plt.plot(x_smooth, smooth_line(df["q_test"]), label="q_test", linewidth=2, color='blue')
plt.plot(x_smooth, smooth_line(df["q_exec"]), label="q_exec", linewidth=2, color='green')

plt.yscale('log')
plt.gca().yaxis.set_major_formatter(ScalarFormatter())
plt.gca().ticklabel_format(style='plain', axis='y')

plt.xlabel("Day", fontsize=35, fontweight='bold')
plt.ylabel("Avg. Waiting Time(s)", fontsize=35, fontweight='bold')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)

plt.legend(fontsize=30, loc='lower right')

plt.tight_layout()
plt.show()
