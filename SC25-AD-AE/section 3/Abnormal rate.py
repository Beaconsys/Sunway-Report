import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# TaihuLight data
df_taihu = pd.DataFrame({
    "year": [2017, 2018, 2019, 2020, 2021, 2022],
    "total_jobs": [501506, 301313, 159926, 2023488, 145155, 30465],
    "done_jobs": [381633, 166078, 86550, 1815045, 91606, 15100],
    "failure_rate": [23.902605352677732, 44.881900216718165, 45.881220064279724,
                     10.301173024006072, 36.89090971719886, 50.43492532414247]
})

# OceanLight data
df_ocean = pd.DataFrame({
    "year": [2021, 2022, 2023, 2024],
    "total_jobs": [296940, 214661, 157063, 222020],
    "done_jobs": [210141, 170266, 112922, 162351],
    "failure_rate": [29.231157809658516, 20.681446559924723, 28.104009219230498,
                     26.87550671110711]
})

all_years = sorted(set(df_taihu["year"]) | set(df_ocean["year"]))
year_index = {year: i + 1 for i, year in enumerate(all_years)}

df_taihu["year_index"] = df_taihu["year"].map(year_index)
df_ocean["year_index"] = df_ocean["year"].map(year_index)

bar_width = 0.4
x_taihu = np.array(df_taihu["year_index"]) - bar_width / 2
x_ocean = np.array(df_ocean["year_index"]) + bar_width / 2

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
