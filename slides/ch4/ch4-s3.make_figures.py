"""第四章 §4.3 插图：封面题图 + 多世界分支示意 + 退相干/量子达尔文主义示意"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot

setup_plot()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

INK = "#20242B"
TEAL = "#1F4E5F"
OCHRE = "#C4622D"
GRAY = "#8A8F98"
PAPER = "#FAF8F4"
LIGHT = "#DCE6EA"
PANEL = "#F3F1EA"
PANEL_TEAL = "#23586B"

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)


def box(ax, x, y, w, h, text, fc, ec, tc, fs=12, weight="normal", lw=1.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.06,rounding_size=0.12",
                                fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, text, color=tc, fontsize=fs,
            ha="center", va="center", weight=weight)


# ---------- 封面题图：经典力学量 -> 量子算符的对应 ----------
fig, ax = plt.subplots(figsize=(4.6, 6.2))
fig.patch.set_facecolor(PANEL_TEAL)
ax.set_facecolor(PANEL_TEAL)

classics = [r"$x$", r"$\mathbf{p}$", r"$\mathbf{L}=\mathbf{r}\times\mathbf{p}$",
            r"$T=\dfrac{p^2}{2m}$", r"$H=T+V$"]
quantums = [r"$\hat{x}=x$", r"$\hat{\mathbf{p}}=-\mathrm{i}\hbar\nabla$",
            r"$\hat{\mathbf{L}}=\mathbf{r}\times\hat{\mathbf{p}}$",
            r"$\hat{T}=\dfrac{\hat{p}^2}{2m}$", r"$\hat{H}=\hat{T}+V$"]

for i, (c, q) in enumerate(zip(classics, quantums)):
    y = 8.6 - i * 1.35
    ax.text(1.7, y, c, color=LIGHT, fontsize=14, ha="center", va="center")
    ax.annotate("", xy=(5.15, y), xytext=(3.05, y),
                arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.8))
    ax.text(7.6, y, q, color="#FFFFFF", fontsize=14, ha="center", va="center")

ax.text(1.7, 9.75, "经典力学量", color="#FFFFFFB3", fontsize=13, ha="center")
ax.text(7.6, 9.75, "厄密算符", color="#FFFFFFB3", fontsize=13, ha="center")
ax.text(4.1, 9.75, "基本假定", color=OCHRE, fontsize=13, ha="center", weight="bold")
ax.text(5.0, 1.35, r"可测值 $=$ 本征值", color=OCHRE, fontsize=15, ha="center")

ax.set_xlim(0, 10)
ax.set_ylim(0.6, 10.4)
ax.axis("off")
fig.savefig(OUT / "fig_cover.png", dpi=220, bbox_inches="tight", facecolor=PANEL_TEAL)
plt.close(fig)


# ---------- 拓展上：埃弗雷特相对态——分支示意 ----------
fig, ax = plt.subplots(figsize=(7.6, 3.6))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

box(ax, 0.2, 2.5, 3.4, 1.5,
    "测量前\n" + r"$\frac{\sqrt{3}}{2}\phi_1+\frac{1}{2}\phi_2$",
    PANEL, GRAY, INK, fs=13)
# 分支①
ax.annotate("", xy=(7.4, 4.35), xytext=(3.9, 3.6),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.8,
                            connectionstyle="arc3,rad=-0.18"))
ax.text(5.35, 4.55, "记录 $+1$", color=TEAL, fontsize=12, ha="center")
box(ax, 7.6, 3.75, 4.2, 1.35,
    "分支①　仪器记录 $+1$\n观察者看到 $+1$",
    "#FFFFFF", TEAL, INK, fs=12)
# 分支②
ax.annotate("", xy=(7.4, 1.15), xytext=(3.9, 1.9),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.8,
                            connectionstyle="arc3,rad=0.18"))
ax.text(5.35, 0.42, "记录 $-1$", color=OCHRE, fontsize=12, ha="center")
box(ax, 7.6, 0.55, 4.2, 1.35,
    "分支②　仪器记录 $-1$\n观察者看到 $-1$",
    "#FFFFFF", OCHRE, INK, fs=12)

ax.text(0.2, 0.1, "相对态表述：不再额外假定「坍缩」，两个分支都保留",
        color=GRAY, fontsize=11.5, ha="left")

ax.set_xlim(0, 12.2)
ax.set_ylim(-0.2, 5.5)
ax.axis("off")
fig.savefig(OUT / "fig_branches.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)


# ---------- 拓展下：退相干 + 量子达尔文主义示意 ----------
fig, ax = plt.subplots(figsize=(8.6, 3.0))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

# 系统
box(ax, 0.2, 1.9, 2.6, 1.2, "系统\n（态 $\\psi$）", PANEL, TEAL, INK, fs=12.5, weight="bold")
# 环境记录
box(ax, 3.8, 0.9, 4.8, 3.0, "", PANEL, GRAY, INK)
ax.text(6.2, 3.42, "环境：散射光子、空气分子……", color=INK, fontsize=11.5, ha="center")
np.random.seed(7)
for i in range(14):
    xx = 4.4 + (i % 5) * 0.82
    yy = 1.5 + (i // 5) * 0.6
    circ = plt.Circle((xx, yy), 0.16, color=TEAL if i % 3 else OCHRE,
                      alpha=0.75 if i % 3 else 0.85)
    ax.add_patch(circ)
ax.text(6.2, 1.06, "携带着系统信息的许多记录", color=GRAY, fontsize=10.5, ha="center")
# 观察者
box(ax, 9.8, 2.75, 2.4, 1.05, "观察者甲\n读到片段①", "#FFFFFF", TEAL, INK, fs=11.5)
box(ax, 9.8, 1.05, 2.4, 1.05, "观察者乙\n读到片段②", "#FFFFFF", OCHRE, INK, fs=11.5)

ax.annotate("", xy=(3.85, 2.5), xytext=(2.95, 2.5),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.6))
ax.annotate("", xy=(9.7, 3.28), xytext=(8.55, 3.05),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.6))
ax.annotate("", xy=(9.7, 1.6), xytext=(8.55, 1.85),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.6))
ax.text(11.0, 4.35, "一致记录", color=INK, fontsize=12, ha="center", weight="bold")

ax.set_xlim(0, 12.6)
ax.set_ylim(0.2, 4.7)
ax.axis("off")
fig.savefig(OUT / "fig_decoherence.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

print("done:", [p.name for p in OUT.glob("*.png")])
