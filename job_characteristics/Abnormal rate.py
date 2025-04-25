import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 仅保留年份和失败率
df_taihu = pd.DataFrame({
    "year": [2017, 2018, 2019, 2020, 2021, 2022],
    "failure_rate": [23.90, 44.88, 45.88, 10.30, 36.89, 50.43]
})

df_ocean = pd.DataFrame({
    "year": [2021, 2022, 2023, 2024],
    "failure_rate": [29.23, 20.68, 28.10, 26.88]
})

# 年份索引
all_years = sorted(set(df_taihu["year"]) | set(df_ocean["year"]))
year_index = {year: i + 1 for i, year in enumerate(all_years)}

df_taihu["year_index"] = df_taihu["year"].map(year_index)
df_ocean["year_index"] = df_ocean["year"].map(year_index)

# 条形图位置
bar_width = 0.4
x_taihu = np.array(df_taihu["year_index"]) - bar_width / 2
x_ocean = np.array(df_ocean["year_index"]) + bar_width / 2

# 画图
plt.rcParams["font.family"] = "Arial"
plt.figure(figsize=(16, 9))
plt.bar(x_taihu, df_taihu["failure_rate"], width=bar_width, label="TaihuLight",
        alpha=1, color="#1f77b4", edgecolor="black")
plt.bar(x_ocean, df_ocean["failure_rate"], width=bar_width, label="OceanLight",
        alpha=1, color="#ff7f0e", edgecolor="black")

plt.xticks(ticks=list(year_index.values()), labels=list(year_index.keys()))
plt.xlabel("Year", fontsize=35, fontweight='bold')
plt.ylabel("Abnormal termination rate (%)", fontsize=35, fontweight='bold')
plt.legend(fontsize=30)
plt.tick_params(axis='both', labelsize=30)
plt.tight_layout()
plt.show()
