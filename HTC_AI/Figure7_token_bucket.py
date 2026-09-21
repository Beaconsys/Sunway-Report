import matplotlib.pyplot as plt
import numpy as np

# Data
categories = ["HTC", "Medium", "Large", "Total time"]
direct_scheduling = [2.35, 7.20, 22.80, 51.00]
token_bucket_throttling = [1.99, 4.99, 17.00, 27.00]

# Global font
plt.rcParams["font.family"] = "Arial"

# Positions
x = np.arange(len(categories))
width = 0.35

# Figure
fig, ax = plt.subplots(figsize=(12, 6))

# Bars
bars1 = ax.bar(
    x - width / 2,
    direct_scheduling,
    width,
    label="Direct scheduling",
    color="#1f77b4",
    edgecolor="black",
    linewidth=1.2
)

bars2 = ax.bar(
    x + width / 2,
    token_bucket_throttling,
    width,
    label="Token bucket throttling",
    color="#ff7f0e",
    edgecolor="black",
    linewidth=1.2
)

# Axes labels and ticks
ax.set_ylabel("Scheduling time (S)", fontsize=25, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=25, fontweight="bold")
ax.tick_params(axis="y", labelsize=20)
ax.tick_params(axis="x", labelsize=25)

# Set Y-axis limit
ax.set_ylim(0, 60)

# Make y-axis tick labels Arial with size 20
for label in ax.get_yticklabels():
    label.set_fontname("Arial")
    label.set_fontsize(20)

# No grid
ax.grid(False)

# Legend with border
legend = ax.legend(
    loc="upper left",
    fontsize=20,
    frameon=True,
    edgecolor="black"
)
legend.get_frame().set_linewidth(1.2)

# Annotate values on bars
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.5,
            f"{height:.2f}",
            ha="center",
            va="bottom",
            fontsize=20
        )

add_labels(bars1)
add_labels(bars2)

# Layout
plt.tight_layout()
plt.show()
fig.savefig("Figure7_token_bucket.pdf", format="pdf", bbox_inches="tight")
print("Saved: Figure7_token_bucket.pdf")
