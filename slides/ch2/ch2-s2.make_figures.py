# -*- coding: utf-8 -*-
"""为量子力学 §2.2 课件生成示意图（配色与 §2.1 一致）"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, FancyBboxPatch
from daimon_runtime import setup_plot

setup_plot()

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)

INK   = "#20242B"
TEAL  = "#1F4E5F"
OCHRE = "#C4622D"
GRAY  = "#8A8F98"
PAPER = "#FAF8F4"

# ---------- 图1：平面波——波前 + Re ψ(x) ----------
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.1), gridspec_kw={"width_ratios": [1, 1.35]})

ax = axes[0]
ax.set_facecolor(PAPER)
lam = 0.5
for i in range(-4, 6):
    ax.axvline(i * lam, color=TEAL, lw=1.6, alpha=0.85)
ax.add_patch(FancyArrowPatch((-1.8, 0), (2.6, 0), arrowstyle="-|>",
             mutation_scale=16, color=OCHRE, lw=2))
ax.text(2.65, 0, r"$\mathbf{k}$（$\mathbf{p}$ 方向）", fontsize=12, color=OCHRE,
        va="center")
ax.annotate("", xy=(0.0, -0.75), xytext=(lam, -0.75),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=1.2))
ax.text(lam / 2, -0.95, "λ", fontsize=13, color=INK, ha="center")
ax.set_xlim(-2.2, 4.2); ax.set_ylim(-1.2, 1.2)
ax.axis("off")
ax.set_title("等相面（波前）：间距 λ = h/p", fontsize=12.5, color=INK)

ax = axes[1]
ax.set_facecolor(PAPER)
x = np.linspace(0, 4 * np.pi, 800)
ax.plot(x, np.cos(x), color=TEAL, lw=2.2)
ax.axhline(0, color=GRAY, lw=0.8)
ax.annotate("", xy=(0, 0.55), xytext=(np.pi * 2, 0.55),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=1.2))
ax.text(np.pi, 0.68, "λ", fontsize=13, color=INK, ha="center")
ax.text(0.25, 1.25, r"$\mathrm{Re}\,\psi(x,t{=}0) = A\cos(px/\hbar)$",
        fontsize=12, color=TEAL)
ax.set_xlim(0, 4 * np.pi); ax.set_ylim(-1.5, 1.6)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel("x", fontsize=11, color=INK)
for sp in ["top", "right"]:
    ax.spines[sp].set_visible(False)
for sp in ["left", "bottom"]:
    ax.spines[sp].set_color(GRAY)
ax.set_title("同一时刻的空间波形：无限延伸、永不衰减", fontsize=12.5, color=INK)

fig.subplots_adjust(left=0.03, right=0.99, top=0.86, bottom=0.10, wspace=0.08)
fig.savefig(OUT / "fig_planewave.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ---------- 图2：均匀几率密度 + 电子束装置 ----------
fig = plt.figure(figsize=(10.5, 3.3))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.5], wspace=0.12)

# 左：Re ψ 振荡 vs |ψ|² 水平线
sub = gs[0].subgridspec(2, 1, hspace=0.55)
ax1 = fig.add_subplot(sub[0]); ax2 = fig.add_subplot(sub[1])
for ax in (ax1, ax2):
    ax.set_facecolor(PAPER)
x = np.linspace(0, 4 * np.pi, 800)
ax1.plot(x, np.cos(x), color=TEAL, lw=1.8)
ax1.set_ylim(-1.4, 1.4); ax1.set_xticks([]); ax1.set_yticks([])
ax1.set_ylabel(r"$\mathrm{Re}\,\psi$", fontsize=11, color=INK)
ax2.plot(x, np.ones_like(x), color=OCHRE, lw=2.6)
ax2.set_ylim(0, 1.8); ax2.set_xticks([]); ax2.set_yticks([])
ax2.set_ylabel(r"$|\psi|^2$", fontsize=11, color=INK)
ax2.set_xlabel("x", fontsize=11, color=INK)
for ax in (ax1, ax2):
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    for sp in ["left", "bottom"]:
        ax.spines[sp].set_color(GRAY)
ax1.set_title("波形振荡，几率密度却是平的：$|A|^2$", fontsize=12.5, color=INK)

# 右：电子束装置示意
ax = fig.add_subplot(gs[1])
ax.set_facecolor(PAPER); ax.axis("off")
ax.set_xlim(0, 12); ax.set_ylim(0, 4)
ax.add_patch(FancyBboxPatch((0.3, 1.5), 1.4, 1.0, boxstyle="round,pad=0.05",
             facecolor="none", edgecolor=INK, lw=1.4))
ax.text(1.0, 2.0, "热灯丝", ha="center", va="center", fontsize=11, color=INK)
ax.add_patch(FancyArrowPatch((1.9, 2.0), (3.1, 2.0), arrowstyle="-|>",
             mutation_scale=13, color=GRAY, lw=1.5))
ax.text(2.5, 2.3, "加速电压 U", ha="center", fontsize=10, color=GRAY)
for yy in (1.1, 2.9):
    ax.add_patch(Rectangle((3.4, yy - 0.55), 0.18, 1.0 if yy < 2 else 1.0,
                 facecolor=INK))
ax.text(3.5, 0.35, "准直缝", ha="center", fontsize=10, color=INK)
# 电子束（均匀圆柱束）
ax.add_patch(Rectangle((4.1, 1.55), 7.2, 0.9, facecolor=TEAL, alpha=0.14,
             edgecolor=TEAL, lw=1.2))
xs_dots = np.random.default_rng(7).uniform(4.2, 11.2, 160)
ys_dots = np.random.default_rng(11).uniform(1.62, 2.38, 160)
ax.scatter(xs_dots, ys_dots, s=3, color=TEAL, alpha=0.8, linewidths=0)
ax.text(7.6, 2.75, "均匀电子束：动量 p 确定、方向一致", ha="center",
        fontsize=11.5, color=TEAL)
ax.text(7.6, 1.1, "束直径 ~0.1 mm —— 对电子而言就是“无限宽”",
        ha="center", fontsize=10.5, color=GRAY)
ax.set_title("平面波描述的不是一个点，而是这束电子中的任一个", fontsize=12.5, color=INK)

fig.subplots_adjust(left=0.06, right=0.99, top=0.86, bottom=0.12)
fig.savefig(OUT / "fig_beam.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ---------- 图3：双缝干涉例题几何图 ----------
fig, ax = plt.subplots(figsize=(6.8, 4.6))
ax.set_facecolor(PAPER); ax.axis("off")
ax.set_xlim(-1.6, 10.5); ax.set_ylim(-3.6, 3.9)

d = 2.0
S1 = np.array([0.0, -d / 2]); S2 = np.array([0.0, d / 2])
B = np.array([9.2, 2.6])
gap = 0.28
# 挡板（两段 + 中间段，留出两条缝）
ax.add_patch(Rectangle((-0.18, -3.3), 0.36, (S1[1] - gap) + 3.3, facecolor=INK))
ax.add_patch(Rectangle((-0.18, S1[1] + gap), 0.36, (S2[1] - gap) - (S1[1] + gap), facecolor=INK))
ax.add_patch(Rectangle((-0.18, S2[1] + gap), 0.36, 3.3 - (S2[1] + gap), facecolor=INK))
ax.text(0.0, -3.55, "挡板", ha="center", fontsize=11, color=INK)
# 缝标注 + d
ax.text(-0.4, S1[1], "$S_1$", ha="right", va="center", fontsize=13, color=TEAL)
ax.text(-0.4, S2[1], "$S_2$", ha="right", va="center", fontsize=13, color=TEAL)
ax.annotate("", xy=(-1.05, S1[1]), xytext=(-1.05, S2[1]),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=1.2))
ax.text(-1.28, 0, "d", fontsize=13, color=INK, ha="center", va="center")
# 两条路径
ax.plot([S1[0], B[0]], [S1[1], B[1]], color=TEAL, lw=1.8)
ax.plot([S2[0], B[0]], [S2[1], B[1]], color=TEAL, lw=1.8)
# 屏
ax.add_patch(Rectangle((9.45, -3.3), 0.25, 6.6, facecolor=INK))
ax.text(9.6, -3.55, "屏", ha="center", fontsize=11, color=INK)
ax.add_patch(Circle(B, 0.09, facecolor=OCHRE, edgecolor="none"))
ax.text(B[0] - 0.15, B[1] + 0.35, "B", fontsize=13, color=OCHRE, ha="center")
# 水平参考线（从 S2 出发）与 θ 角
ax.plot([S2[0], B[0]], [S2[1], S2[1]], ls="--", color=GRAY, lw=1.0)
ax.text(6.4, S2[1] + 0.14, "l", fontsize=12, color=GRAY, ha="center")
theta_deg = np.degrees(np.arctan2(B[1] - S2[1], B[0] - S2[0]))
arc = matplotlib.patches.Arc(S2, 5.6, 5.6, angle=0, theta1=0, theta2=theta_deg,
                             color=INK, lw=1.2)
ax.add_patch(arc)
mid = np.radians(theta_deg / 2)
ax.text(S2[0] + 3.1 * np.cos(mid) + 0.1, S2[1] + 3.1 * np.sin(mid), "θ",
        fontsize=13, color=INK)
# 程差 Δ：从 S1 向 S2B 作垂线
v = (B - S2) / np.linalg.norm(B - S2)
foot = S2 + v * np.dot(S1 - S2, v)
ax.plot([S1[0], foot[0]], [S1[1], foot[1]], color=OCHRE, lw=1.4)
ax.plot([S2[0], foot[0]], [S2[1], foot[1]], color=OCHRE, lw=3.0)
# 直角符号
s = 0.26
u = (S1 - foot) / np.linalg.norm(S1 - foot)
w = -v
p1 = foot + w * s
p2 = foot + w * s + u * s
p3 = foot + u * s
ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color=OCHRE, lw=1.0)
midpt = (S2 + foot) / 2
ax.text(midpt[0] + 0.5, midpt[1] - 0.55, "Δ = d sinθ", fontsize=12.5, color=OCHRE)
ax.text(4.8, 3.5, "d ≪ l：两条路径近似平行", fontsize=11.5, color=GRAY, ha="center")
fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
fig.savefig(OUT / "fig_dslit_geo.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ---------- 图4：波包 = 平面波叠加 ----------
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.3))

ax = axes[0]; ax.set_facecolor(PAPER)
x = np.linspace(-30, 30, 3000)
k0 = 1.0
rngk = np.linspace(0.75, 1.25, 5)
for k in rngk:
    ax.plot(x, 0.35 * np.cos(k * x), color=GRAY, lw=0.8, alpha=0.6)
sigma = 8.0
packet = np.cos(k0 * x) * np.exp(-x**2 / (2 * sigma**2))
ax.plot(x, packet, color=TEAL, lw=2.4)
ax.set_ylim(-1.5, 1.5); ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel("x", fontsize=11, color=INK)
for sp in ["top", "right"]:
    ax.spines[sp].set_visible(False)
for sp in ["left", "bottom"]:
    ax.spines[sp].set_color(GRAY)
ax.set_title("若干动量相近的平面波（灰）叠加 → 波包（青）", fontsize=12.5, color=INK)

ax = axes[1]; ax.set_facecolor(PAPER)
density = np.exp(-x**2 / sigma**2)
ax.plot(x, density, color=OCHRE, lw=2.4)
ax.fill_between(x, density, color=OCHRE, alpha=0.12)
ax.annotate("", xy=(-sigma, 0.42), xytext=(sigma, 0.42),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=1.2))
ax.text(0, 0.5, "Δx", fontsize=13, color=INK, ha="center")
ax.set_ylim(0, 1.3); ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel("x", fontsize=11, color=INK)
for sp in ["top", "right"]:
    ax.spines[sp].set_visible(False)
for sp in ["left", "bottom"]:
    ax.spines[sp].set_color(GRAY)
ax.set_title(r"$|\psi|^2$ 局域了：代价是动量展宽 $\Delta p \sim \hbar/\Delta x$",
             fontsize=12.5, color=INK)

fig.subplots_adjust(left=0.04, right=0.99, top=0.86, bottom=0.12, wspace=0.10)
fig.savefig(OUT / "fig_wavepacket.png", dpi=200, facecolor=PAPER)
plt.close(fig)

print("done:", [p.name for p in OUT.glob("*.png")])
