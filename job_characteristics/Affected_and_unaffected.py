import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Arial"
plt.rcParams["xtick.labelsize"] = 20
plt.rcParams["ytick.labelsize"] = 20

# TaihuLight
abnormal_affected1 = [
    55.32, 67.57, 7.65, 34.69, 20.0, 7.07, 18.6, 16.07, 48.44, 54.55, 6.45, 17.7, 3.72, 6.61, 14.86, 49.61,
    44.09, 47.12, 0.82, 4.74, 21.19, 47.96, 29.73, 50.0, 39.33, 21.05, 40.54, 12.5
]
abnormal_unaffected1 = [
    41.17, 40.03, 9.6, 13.76, 23.16, 3.38, 0.43, 6.17, 27.51, 24.29, 1.47, 20.99, 3.93, 5.62, 12.22, 26.68,
    32.25, 10.7, 0.43, 3.7, 14.89, 23.04, 10.95, 37.7, 46.45, 14.87, 31.8, 25.1
]

# OceanLight
abnormal_affected2 = [
    0.0, 7.14, 28.0, 40.0, 2.86, 38.46, 58.82, 53.85, 12.5, 19.23, 59.52, 66.67,
    30.77, 19.05, 7.5, 13.04, 5.56, 16.67, 15.56, 0.97, 28.95, 6.67, 18.18, 26.39,
    50.0, 46.15, 3.45, 30.0, 5.71
]
abnormal_unaffected2 = [
    4.98, 9.82, 26.31, 2.41, 2.6, 5.55, 16.67, 14.41, 6.82, 10.41, 43.54, 32.29,
    23.1, 12.18, 8.2, 9.12, 4.54, 16.23, 0.89, 2.39, 10.5, 6.61, 8.88, 25.86,
    9.0, 8.41, 3.61, 15.87, 4.39
]

# -------- TaihuLight fig --------
plt.figure(figsize=(10, 9))
x1 = list(range(1, len(abnormal_affected1) + 1))
plt.plot(x1, abnormal_affected1, label="Affected Jobs", color='r', linewidth=2)
plt.plot(x1, abnormal_unaffected1, label="Unaffected Jobs", color='b', linewidth=2)
plt.legend(fontsize=30)
plt.xlabel("Day", fontsize=35, fontweight='bold')
plt.ylabel("Abnormal Termination Rate (%)", fontsize=35, fontweight='bold')
xticks1 = list(range(0, len(abnormal_affected1), 5))
plt.xticks(ticks=xticks1, labels=[str(i + 1) for i in xticks1])
plt.tick_params(axis='both', labelsize=30)
plt.tick_params(axis='both', which='both', direction='in', length=6)
plt.grid(False)
plt.tight_layout()
plt.show()

# -------- OceanLight fig --------
plt.figure(figsize=(10, 9))
x2 = list(range(1, len(abnormal_affected2) + 1))
plt.plot(x2, abnormal_affected2, label="Affected Jobs", color='r', linewidth=2)
plt.plot(x2, abnormal_unaffected2, label="Unaffected Jobs", color='b', linewidth=2)
plt.legend(fontsize=30)
plt.xlabel("Day", fontsize=35, fontweight='bold')
plt.ylabel("Abnormal Termination Rate (%)", fontsize=35, fontweight='bold')
xticks2 = list(range(0, len(abnormal_affected2), 5))
plt.xticks(ticks=xticks2, labels=[str(i + 1) for i in xticks2])
plt.tick_params(axis='both', labelsize=30)
plt.tick_params(axis='both', which='both', direction='in', length=6)
plt.grid(False)
plt.tight_layout()
plt.show()
