# -*- coding: utf-8 -*-
"""为量子力学 §2.1 课件生成示意图（全部透明背景，配色与课件一致）"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
from matplotlib.colors import LinearSegmentedColormap
from daimon_runtime import setup_plot

setup_plot()

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)

INK   = "#20242B"   # 近黑
TEAL  = "#1F4E5F"   # 结构色
OCHRE = "#C4622D"   # 强调色
GRAY  = "#8A8F98"   # 辅助灰
PAPER = "#FAF8F4"

rng = np.random.default_rng(20260907)

# ---------- 共同的几率分布 ----------
# 双缝：条纹 cos^2(pi x / d) 乘以高斯包络
d_fringe = 0.5
sigma = 1.35
xs = np.linspace(-3, 3, 1201)
envelope = np.exp(-xs**2 / (2 * sigma**2))
P12 = np.cos(np.pi * xs / d_fringe)**2 * envelope
# 单缝：各自错开的高斯包络
shift = 0.45
P1 = np.exp(-(xs + shift)**2 / (2 * sigma**2)) * 0.5
P2 = np.exp(-(xs - shift)**2 / (2 * sigma**2)) * 0.5

def sample_points(n, pdf, xs, yrange=(-1.0, 1.0)):
    """按 pdf 拒绝采样 x，y 均匀"""
    cdf = np.cumsum(pdf)
    cdf /= cdf[-1]
    u = rng.random(n)
    x = np.interp(u, cdf, xs)
    y = rng.uniform(*yrange, n)
    return x, y

# ---------- 图1：点子逐步累积成条纹（4 帧） ----------
counts = [10, 200, 3000, 30000]
fig, axes = plt.subplots(1, 4, figsize=(12, 3.0))
for ax, n in zip(axes, counts):
    x, y = sample_points(n, P12, xs)
    s = 18 if n <= 200 else (2.5 if n <= 3000 else 0.35)
    ax.scatter(x, y, s=s, c="white", alpha=0.9, linewidths=0)
    ax.set_facecolor("#10151B")
    ax.set_xlim(-3, 3); ax.set_ylim(-1, 1)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color(GRAY); sp.set_linewidth(0.8)
    ax.set_title(f"{n:,} 个电子", color=INK, fontsize=13, pad=8)
fig.subplots_adjust(left=0.01, right=0.99, top=0.82, bottom=0.02, wspace=0.06)
fig.savefig(OUT / "fig_buildup.png", dpi=200, transparent=False, facecolor=PAPER)
plt.close(fig)

# ---------- 图2：单缝几率 vs 双缝几率 ----------
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.6))

ax = axes[0]
ax.plot(xs, P1, color=TEAL, lw=2, label=r"只开缝 $S_1$：$P_1=|\psi_1|^2$")
ax.plot(xs, P2, color=OCHRE, lw=2, label=r"只开缝 $S_2$：$P_2=|\psi_2|^2$")
ax.fill_between(xs, P1, color=TEAL, alpha=0.10)
ax.fill_between(xs, P2, color=OCHRE, alpha=0.10)
ax.set_title("每次只开一条缝", fontsize=13, color=INK)
ax.legend(fontsize=11, frameon=False, loc="upper right")

ax = axes[1]
ax.plot(xs, (P1 + P2) * 1.06, color=GRAY, lw=2, ls="--",
        label=r"几率直接相加：$P_1+P_2$")
ax.plot(xs, P12, color=TEAL, lw=2.4,
        label=r"实验结果：$P_{12}=|\psi_1+\psi_2|^2$")
ax.fill_between(xs, P12, color=TEAL, alpha=0.12)
ax.set_title("两条缝同时打开", fontsize=13, color=INK)
ax.legend(fontsize=11, frameon=False, loc="upper right")

for ax in axes:
    ax.set_facecolor(PAPER)
    ax.set_xlim(-3, 3); ax.set_ylim(0, 1.25)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("屏上位置 x", fontsize=11, color=INK)
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    for sp in ["left", "bottom"]:
        ax.spines[sp].set_color(GRAY)
fig.subplots_adjust(left=0.04, right=0.99, top=0.86, bottom=0.13, wspace=0.10)
fig.savefig(OUT / "fig_curves.png", dpi=200, transparent=False, facecolor=PAPER)
plt.close(fig)

# ---------- 装置示意图的公共绘制函数 ----------
def draw_apparatus(ax, with_detector=False, fringe=True):
    """画双缝装置：电子源 → 双缝挡板 → 屏（带分布曲线）"""
    ax.set_xlim(0, 10); ax.set_ylim(0, 4)
    ax.axis("off")
    # 电子源
    ax.add_patch(Circle((0.7, 2.0), 0.22, facecolor=INK, edgecolor="none"))
    ax.text(0.7, 1.35, "电子源", ha="center", fontsize=11, color=INK)
    # 入射箭头
    ax.add_patch(FancyArrowPatch((1.15, 2.0), (2.6, 2.0),
                 arrowstyle="-|>", mutation_scale=14, color=GRAY, lw=1.5))
    # 挡板（两条缝）
    wall_x = 3.0
    ax.add_patch(Rectangle((wall_x - 0.10, 0.5), 0.20, 1.05, facecolor=INK))
    ax.add_patch(Rectangle((wall_x - 0.10, 1.85), 0.20, 0.30, facecolor=INK))
    ax.add_patch(Rectangle((wall_x - 0.10, 2.45), 0.20, 1.05, facecolor=INK))
    ax.text(wall_x, 0.18, "挡板", ha="center", fontsize=11, color=INK)
    ax.text(wall_x - 0.35, 1.62, "$S_1$", ha="right", fontsize=12, color=TEAL)
    ax.text(wall_x - 0.35, 2.28, "$S_2$", ha="right", fontsize=12, color=TEAL)
    # 探测器
    if with_detector:
        for yy in (1.70, 2.30):
            ax.add_patch(Circle((wall_x + 0.42, yy), 0.16, facecolor="none",
                                edgecolor=OCHRE, lw=2))
            ax.text(wall_x + 0.42, yy - 0.015, "D", ha="center", va="center",
                    fontsize=9, color=OCHRE, fontweight="bold")
        ax.text(wall_x + 0.42, 2.78, "探测器", ha="center", fontsize=10, color=OCHRE)
    # 从两条缝到屏的虚线
    for yy in (1.70, 2.30):
        ax.plot([wall_x + 0.10, 7.6], [yy, 2.0], ls=":", lw=0.9, color=GRAY)
    # 屏
    screen_x = 7.8
    ax.add_patch(Rectangle((screen_x, 0.5), 0.16, 3.0, facecolor=INK))
    ax.text(screen_x + 0.08, 0.18, "探测屏", ha="center", fontsize=11, color=INK)
    # 屏旁的分布曲线（横躺）
    xcurve = np.linspace(0.5, 3.5, 400)
    if fringe:
        p = np.cos(np.pi * (xcurve - 2.0) / 0.5)**2 * np.exp(-(xcurve - 2.0)**2 / 1.2)
        col = TEAL
    else:
        p = np.exp(-(xcurve - 2.0)**2 / 1.2)
        col = GRAY
    ax.plot(screen_x + 0.16 + p * 1.5, xcurve, color=col, lw=2)

# ---------- 图3：双缝装置示意（单幅） ----------
fig, ax = plt.subplots(figsize=(10, 2.4))
draw_apparatus(ax, with_detector=False, fringe=True)
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
fig.savefig(OUT / "fig_setup.png", dpi=200, transparent=False, facecolor=PAPER)
plt.close(fig)

# ---------- 图4：观测 vs 不观测 ----------
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.4))
draw_apparatus(axes[0], with_detector=False, fringe=True)
axes[0].set_title("不观测路径：出现干涉条纹", fontsize=13, color=INK, pad=6)
draw_apparatus(axes[1], with_detector=True, fringe=False)
axes[1].set_title("在缝口观测路径：条纹消失", fontsize=13, color=INK, pad=6)
fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.02, wspace=0.05)
fig.savefig(OUT / "fig_whichpath.png", dpi=200, transparent=False, facecolor=PAPER)
plt.close(fig)

# ---------- 图5：封面竖条纹装饰 ----------
cmap = LinearSegmentedColormap.from_list("fringe", [PAPER, TEAL])
xx = np.linspace(0, 1, 600)
pattern = np.cos(np.pi * xx / 0.09)**2 * np.exp(-(xx - 0.5)**2 / 0.16)
pattern = np.tile(pattern, (80, 1))
fig, ax = plt.subplots(figsize=(4.2, 7.5))
ax.imshow(pattern, cmap=cmap, aspect="auto", vmin=0, vmax=1.15)
ax.axis("off")
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
fig.savefig(OUT / "fig_cover.png", dpi=200, transparent=False, facecolor=PAPER)
plt.close(fig)

print("done:", [p.name for p in OUT.glob("*.png")])
