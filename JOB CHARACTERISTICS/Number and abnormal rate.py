import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.family'] = 'Arial'

# TaihuLight data
data1 = {
    'Index': list(range(1, 25)),
    'Total Leadership Jobs': [
        17700, 17500, 15210, 15180, 15160, 15140, 15150, 15205,
        17400, 20010, 21750, 20020, 19850, 20750, 22000, 22070,
        21900, 19950, 18200, 17700, 17902, 17905, 18105, 17903
    ],
    'Abnormal Rate of Small-Scale Jobs': [
        16.5, 13, 12.5, 11, 10.4, 9.9, 10.1, 11.5,
        17, 21.25, 22.7, 20.65, 17.5, 20.25, 24.25, 28.3,
        27.5, 22.1, 19.65, 21, 21.97, 21.95, 20.25, 18.75
    ]
}

# OceanLight data
data2 = {
    'Index': list(range(1, 25)),
    'Total Leadership Jobs': [
        3800, 3433.333333, 2516.666667, 1916.666667, 1666.666667, 1450,
        1400, 1933.333333, 3633.333333, 7783.333333, 8500, 9300,
        7983.333333, 7633.333333, 6816.666667, 7833.333333,
        8566.666667, 7133.333333, 5116.666667, 5533.333333,
        6316.666667, 5550, 5883.333333, 6033.333333
    ],
    'Abnormal Rate of Small-Scale Jobs': [
        17.6171875, 16.71875, 14.53125, 14.7265625, 11.171875, 12.109375,
        9.296875, 17.421875, 21.9921875, 30.8984375, 28.359375, 30.859375,
        18.6328125, 24.9609375, 31.8359375, 31.796875, 34.296875,
        25.3125, 23.125, 25.0390625, 24.53125, 27.109375,
        25.2734375, 21.8359375
    ]
}

def plot_combined(data_dict, bar_color="#1f77b4"):
    df = pd.DataFrame(data_dict)

    fig, ax1 = plt.subplots(figsize=(9, 9))

    bars = ax1.bar(
        df['Index'],
        df['Total Leadership Jobs'],
        alpha=1,
        color=bar_color,
        edgecolor="black",
        label="Total Leadership Jobs"
    )

    ax1.tick_params(axis='both', labelsize=30)
    ax1.set_ylabel("Large-Scale Job's Number", fontsize=35,fontweight='bold')
    ax1.set_xlabel("Hour", fontsize=35,fontweight='bold')

    ax2 = ax1.twinx()
    ax2.plot(
        df['Index'],
        df['Abnormal Rate of Small-Scale Jobs'],
        color='#ff0000',  # 更鲜艳的红色
        linewidth=3,
        label='Abnormal Rate of Small-Scale Jobs'
    )
    ax2.set_ylabel("Abnormal Termination Rate(%)", fontsize=35,fontweight='bold')
    ax2.tick_params(axis='y', labelsize=30)
    ax2.set_ylim(9, 35)

    ax1.set_xticks([0, 4, 8, 12, 16, 20, 24])

    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    ax = plt.gca()
    ax.yaxis.get_offset_text().set_fontsize(30)

    plt.tight_layout()
    plt.show()


# 绘制两张图
plot_combined(data1)
plot_combined(data2)
