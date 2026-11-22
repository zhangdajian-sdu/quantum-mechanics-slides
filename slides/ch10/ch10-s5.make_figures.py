import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
import numpy as np
import matplotlib.pyplot as plt
from daimon_runtime import setup_plot

setup_plot()

INK = "#20242B"
TEAL = "#1F4E5F"
OCHRE = "#C4622D"
GRAY = "#8A8F98"
PAPER = "#FAF8F4"

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print("saved", name)


# ---------- 封面：两个自旋 1/2 → 三重态与单态（teal 底，竖版） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

# 两个粒子
ax.plot(-1.7, 1.9, "o", ms=26, color="#FAF8F4")
ax.plot(1.7, 1.9, "o", ms=26, color="#E8B48C")
ax.annotate("", xy=(-1.7, 2.6), xytext=(-1.7, 1.9),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.4))
ax.annotate("", xy=(1.7, 2.6), xytext=(1.7, 1.9),
            arrowprops=dict(arrowstyle="-|>", color="#7A2E12", lw=2.4))
ax.text(-1.7, 1.15, "入射粒子", color="#FAF8F4", fontsize=12, ha="center")
ax.text(1.7, 1.15, "靶粒子", color="#E8B48C", fontsize=12, ha="center")
ax.text(0, 2.15, "+", color="#FAF8F4", fontsize=20, ha="center")

# 耦合结果
ax.text(-1.9, -0.35, "三重态 S=1（3 个态）", color="#FAF8F4", fontsize=13, ha="center")
ax.text(-1.9, -0.9, r"$V_3=V_0+\dfrac{\hbar^{2}}{4}g(r)$", color="#FAF8F4",
        fontsize=13, ha="center")
ax.text(1.9, -0.35, "单态 S=0（1 个态）", color="#FAF8F4", fontsize=13, ha="center")
ax.text(1.9, -0.9, r"$V_1=V_0-\dfrac{3\hbar^{2}}{4}g(r)$", color="#FAF8F4",
        fontsize=13, ha="center")
ax.plot([0, 0], [-1.35, 0.35], color="#FAF8F4", lw=1.0, alpha=0.4)

ax.text(0, -2.6, r"$\sigma=|f_3|^{2}w_3+|f_1|^{2}w_1$", color="#E8B48C",
        fontsize=16, ha="center")

ax.set_xlim(-4.4, 4.4)
ax.set_ylim(-4.9, 4.0)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 三重态与单态的等效势（g>0 示意） ----------
fig, ax = plt.subplots(figsize=(7.2, 3.0), facecolor=PAPER)
ax.set_facecolor(PAPER)

ax.plot([0.4, 2.4], [0, 0], color=INK, lw=2.4)
ax.text(1.4, 0.14, r"$V_0$", ha="center", fontsize=12, color=INK)

ax.plot([3.6, 5.6], [0.75, 0.75], color=TEAL, lw=2.4)
ax.text(4.6, 0.9, r"$V_3=V_0+\dfrac{\hbar^{2}}{4}g$（三重态，3 个）", ha="center",
        fontsize=11.5, color=TEAL)
ax.plot([3.6, 5.6], [-0.75, -0.75], color=OCHRE, lw=2.4)
ax.text(4.6, -1.02, r"$V_1=V_0-\dfrac{3\hbar^{2}}{4}g$（单态，1 个）", ha="center",
        fontsize=11.5, color=OCHRE)

ax.annotate("", xy=(3.05, 0.75), xytext=(3.05, 0),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.5))
ax.annotate("", xy=(3.05, -0.75), xytext=(3.05, 0),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.5))
ax.text(3.17, 0.32, r"$+\frac{\hbar^{2}}{4}g$", color=TEAL, fontsize=11)
ax.text(3.17, -0.62, r"$-\frac{3\hbar^{2}}{4}g$", color=OCHRE, fontsize=11)

ax.text(7.0, 0.3, "S²、$S_z$ 守恒 ⇒", fontsize=12, color=INK)
ax.text(7.0, -0.15, "两类态各自独立散射", fontsize=12, color=INK)

ax.set_xlim(0, 9.4)
ax.set_ylim(-1.45, 1.35)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_levels.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
