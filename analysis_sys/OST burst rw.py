# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker

plt.rcParams["font.family"] = "Arial"
plt.rcParams["axes.labelsize"] = 35
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["xtick.labelsize"] = 30
plt.rcParams["ytick.labelsize"] = 30
plt.rcParams["legend.fontsize"] = 30

read_df = pd.read_csv('read_burst.csv', header=None, names=["Start", "End", "Duration_sec", "Avg_IO_MBps"])
write_df = pd.read_csv('write_burst.csv', header=None, names=["Start", "End", "Duration_sec", "Avg_IO_MBps"])

def categorize_duration_seconds(duration):
    if duration <= 10:
        return '(0,10]'
    elif 10 < duration <= 30:
        return '(10,30]'
    elif 30 < duration <= 120:
        return '(30,120]'
    else:
        return '(120,∞)'

def categorize_io(io_value):
    if io_value <= 30:
        return '(0,30]'
    elif 30 < io_value <= 60:
        return '(30,60]'
    elif 60 < io_value <= 90:
        return '(60,90]'
    else:
        return '(90,∞)'

read_df['Duration Category'] = read_df['Duration_sec'].apply(categorize_duration_seconds)
write_df['Duration Category'] = write_df['Duration_sec'].apply(categorize_duration_seconds)

read_df['IO Category'] = read_df['Avg_IO_MBps'].apply(lambda x: categorize_io(x / 1024))  # MB/s -> GB/s
write_df['IO Category'] = write_df['Avg_IO_MBps'].apply(lambda x: categorize_io(x / 1024))

duration_categories = ['(0,10]', '(10,30]', '(30,120]', '(120,∞)']
io_categories = ['(0,30]', '(30,60]', '(60,90]', '(90,∞)']

read_duration_counts = read_df['Duration Category'].value_counts().reindex(duration_categories, fill_value=0)
write_duration_counts = write_df['Duration Category'].value_counts().reindex(duration_categories, fill_value=0)

read_io_counts = read_df['IO Category'].value_counts().reindex(io_categories, fill_value=0)
write_io_counts = write_df['IO Category'].value_counts().reindex(io_categories, fill_value=0)

# ========= Duration =========
fig, ax1 = plt.subplots(figsize=(10, 7.2))

x_duration = np.arange(len(duration_categories))
width = 0.35

ax1.bar(x_duration - width/2, read_duration_counts, width, label='Read', color='#1f77b4', edgecolor='black')
ax1.bar(x_duration + width/2, write_duration_counts, width, label='Write', color='#ff7f0e', edgecolor='black')

ax1.set_xlabel('Duration (Seconds)')
ax1.set_ylabel('Burst Count')
ax1.set_xticks(x_duration)
ax1.set_xticklabels(duration_categories)
ax1.legend()
ax1.set_yscale('log')
ax1.set_ylim(bottom=1)

# 关闭科学计数法
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x)}'))

plt.tight_layout()
plt.show()

# ========= I/O Volume =========
fig, ax2 = plt.subplots(figsize=(10, 7.2))

x_io = np.arange(len(io_categories))

ax2.bar(x_io - width/2, read_io_counts, width, label='Read', color='#1f77b4', edgecolor='black')
ax2.bar(x_io + width/2, write_io_counts, width, label='Write', color='#ff7f0e', edgecolor='black')

ax2.set_xlabel('I/O Volume (GB/s)')
ax2.set_ylabel('Burst Count')
ax2.set_xticks(x_io)
ax2.set_xticklabels(io_categories)
ax2.legend()
ax2.set_yscale('log')
ax2.set_ylim(bottom=1)

ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x)}'))

plt.tight_layout()
plt.show()
