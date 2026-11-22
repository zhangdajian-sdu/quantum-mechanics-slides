# -*- coding: utf-8 -*-
"""ch6-s1 简单的三维定态问题 — 配图生成"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from daimon_runtime import setup_plot

setup_plot()

INK = "#20242B"
TEAL = "#1F4E5F"
OCHRE = "#C4622D"
GRAY = "#8A8F98"
PAPER = "#FAF8F4"
HAIR = "#E2DFD8"

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print("saved", name)


# ---------- 封面图：三维方盒中的驻波 ----------
fig = plt.figure(figsize=(6.0, 7.2), facecolor=TEAL)
ax = fig.add_subplot(111, projection="3d")
ax.set_facecolor(TEAL)

# 半透明盒子
r = [0, 1]
for s, e in [((0,0,0),(1,1,0)), ((0,0,1),(1,1,1)),
             ((0,0,0),(0,1,1)), ((1,0,0),(1,1,1)),
             ((0,0,0),(1,0,1)), ((0,1,0),(1,1,1))]:
    pass
# 盒子的 12 条棱
edges = [
    ((0,0,0),(1,0,0)), ((0,0,0),(0,1,0)), ((0,0,0),(0,0,1)),
    ((1,1,0),(1,0,0)), ((1,1,0),(0,1,0)), ((1,1,0),(1,1,1)),
    ((1,0,1),(1,0,0)), ((1,0,1),(0,0,1)), ((1,0,1),(1,1,1)),
    ((0,1,1),(0,1,0)), ((0,1,1),(0,0,1)), ((0,1,1),(1,1,1)),
]
for a, b in edges:
    xs = [a[0], b[0]]; ys = [a[1], b[1]]; zs = [a[2], b[2]]
    ax.plot(xs, ys, zs, color="#FFFFFF", lw=1.4, alpha=0.9)

# 盒内一个 (2,1,1) 模式的驻波切片（z=0.5 平面）
n = 60
x = np.linspace(0, 1, n)
y = np.linspace(0, 1, n)
X, Y = np.meshgrid(x, y)
Z = 0.5 * np.ones_like(X)
W = np.sin(2 * np.pi * X) * np.sin(np.pi * Y) * np.sin(np.pi * Z)
ax.plot_surface(X, Y, Z + 0.28 * W, cmap="coolwarm", alpha=0.85,
                linewidth=0, antialiased=True)

ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 1.1)
ax.set_axis_off()
ax.view_init(elev=18, azim=-58)
fig.text(0.5, 0.06, "三维无限深方势阱中的一个驻波模式",
         ha="center", color="#FFFFFFCC", fontsize=12)
save(fig, "fig_cover.png")


# ---------- 导言图：一维阱 vs 三维盒 ----------
fig, axes = plt.subplots(1, 2, figsize=(8.2, 4.4), facecolor=PAPER)

# 左：一维无限深阱 + 两个能级驻波
ax = axes[0]
ax.set_facecolor(PAPER)
x = np.linspace(-0.15, 1.15, 400)
V = np.where((x >= 0) & (x <= 1), 0.0, 1.0)
ax.plot(x, V, color=INK, lw=2)
x1 = np.linspace(0, 1, 200)
ax.plot(x1, 0.18 + 0.10 * np.sin(np.pi * x1), color=OCHRE, lw=1.8)
ax.plot(x1, 0.45 + 0.10 * np.sin(2 * np.pi * x1), color=TEAL, lw=1.8)
ax.text(0.5, -0.16, "一维：一条曲线  $E_n \\propto n^2$", ha="center",
        fontsize=12, color=INK)
ax.set_xlim(-0.15, 1.15); ax.set_ylim(-0.25, 1.15)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)

# 右：三维盒子（轴测示意）
ax = axes[1]
ax.set_facecolor(PAPER)
# 用斜投影画盒子
def proj(p):
    return (p[0] + 0.38 * p[2], p[1] + 0.30 * p[2])
verts = [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]
face = [verts[0], verts[1], verts[2], verts[3], verts[0]]
for loop, col, lw, alpha in [
    ([verts[0],verts[1],verts[2],verts[3],verts[0]], INK, 2, 1),
    ([verts[4],verts[5],verts[6],verts[7],verts[4]], INK, 2, 1),
    ([verts[0],verts[4]], INK, 2, 1),
    ([verts[1],verts[5]], INK, 2, 1),
    ([verts[2],verts[6]], INK, 2, 1),
    ([verts[3],verts[7]], INK, 2, 1),
]:
    xs = [proj(p)[0] for p in loop]; ys = [proj(p)[1] for p in loop]
    ax.plot(xs, ys, color=col, lw=lw, alpha=alpha)
# 盒内三条一维驻波提示
t = np.linspace(0, 1, 200)
ax.plot(t, 0.16 + 0.07*np.sin(3*np.pi*t), color=OCHRE, lw=1.5)
ax.plot(t + 0.38*0.55, 0.5 + 0.30*0.55 + 0.06*np.sin(2*np.pi*t),
        color=TEAL, lw=1.5)
ax.text(0.72, -0.16, "三维：三个量子数  $E \\propto n_1^2+n_2^2+n_3^2$",
        ha="center", fontsize=12, color=INK)
ax.set_xlim(-0.1, 1.55); ax.set_ylim(-0.25, 1.55)
ax.set_xticks([]); ax.set_yticks([])
ax.set_aspect("equal")
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_intro.png")


# ---------- 立方阱能级与简并 ----------
# E / (pi^2 hbar^2 / 2 mu a^2) = n1^2+n2^2+n3^2
levels = {}
from itertools import product
for n1, n2, n3 in product(range(1, 5), repeat=3):
    e = n1**2 + n2**2 + n3**2
    levels.setdefault(e, 0)
    levels[e] += 1
es = sorted(levels)[:6]
fig, ax = plt.subplots(figsize=(7.6, 4.6), facecolor=PAPER)
ax.set_facecolor(PAPER)
for e in es:
    deg = levels[e]
    ax.hlines(e, 0.1, 0.62, color=INK, lw=2)
    label = f"{e}"
    ax.text(0.08, e, label, ha="right", va="center", fontsize=12, color=INK)
    # 简并度标记：叠放小圆点
    for k in range(deg):
        ax.plot(0.68 + 0.045 * k, e, "o", ms=7, color=OCHRE,
                mec=OCHRE, mfc=OCHRE)
    ax.text(0.68 + 0.045 * deg + 0.02, e,
            f"{deg} 重简并" if deg > 1 else "不简并",
            ha="left", va="center", fontsize=11,
            color=OCHRE if deg > 1 else GRAY)
# 标注几个量子数组合
combos = {3: "(1,1,1)", 6: "(2,1,1) 等", 9: "(2,2,1) 等", 12: "(2,2,2)"}
for e, c in combos.items():
    if e in es:
        ax.text(0.33, e + 0.32, c, ha="center", fontsize=10, color=GRAY)
ax.set_xlim(0, 1.15)
ax.set_ylim(1.5, max(es) + 2)
ax.set_yticks([])
ax.set_xticks([])
for s in ["top", "right", "bottom"]:
    ax.spines[s].set_visible(False)
ax.spines["left"].set_color(HAIR)
ax.set_ylabel("$E\\;/\\;(\\pi^2\\hbar^2/2\\mu a^2)$", fontsize=13)
save(fig, "fig_cube.png")


# ---------- 各向同性谐振子能级与简并 ----------
fig, ax = plt.subplots(figsize=(7.6, 4.6), facecolor=PAPER)
ax.set_facecolor(PAPER)
for N in range(0, 5):
    E = N + 1.5
    deg = (N + 1) * (N + 2) // 2
    ax.hlines(E, 0.1, 0.62, color=INK, lw=2)
    ax.text(0.08, E, f"$N={N}$", ha="right", va="center", fontsize=12, color=INK)
    for k in range(deg):
        ax.plot(0.68 + 0.04 * k, E, "o", ms=6.5, color=TEAL)
    ax.text(0.68 + 0.04 * deg + 0.02, E, f"{deg}", ha="left", va="center",
            fontsize=11.5, color=TEAL, fontweight="bold")
ax.text(0.68, 6.35, "简并度 $\\frac{(N+1)(N+2)}{2}$", fontsize=12, color=GRAY)
ax.set_xlim(0, 1.15)
ax.set_ylim(1.0, 6.8)
ax.set_xticks([])
ax.set_yticks([1.5, 2.5, 3.5, 4.5, 5.5],
              ["$\\frac{3}{2}$", "$\\frac{5}{2}$", "$\\frac{7}{2}$",
               "$\\frac{9}{2}$", "$\\frac{11}{2}$"], fontsize=11)
for s in ["top", "right", "bottom"]:
    ax.spines[s].set_visible(False)
ax.spines["left"].set_color(HAIR)
ax.set_ylabel("$E_N\\,/\\,\\hbar\\omega$", fontsize=13)
save(fig, "fig_osc.png")


# ---------- 课外页图：量子点 ----------
fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=PAPER)
ax.set_facecolor(PAPER)
# 纳米晶示意：中心小球 + 离散能级 + 发光颜色随尺寸变化
sizes = [2.0, 3.2, 4.8]
colors = ["#3A6FB0", "#4CAF7D", "#C4622D"]
names = ["小量子点", "中等", "大量子点"]
for i, (s, c, nm) in enumerate(zip(sizes, colors, names)):
    cx = 0.18 + i * 0.32
    circle = plt.Circle((cx, 0.62), 0.035 * s / 2, color=c, alpha=0.9)
    ax.add_patch(circle)
    ax.text(cx, 0.40, nm, ha="center", fontsize=11, color=INK)
    # 发光波长箭头
    lam = 470 + i * 90
    ax.annotate("", xy=(cx + 0.10, 0.24), xytext=(cx, 0.30),
                arrowprops=dict(arrowstyle="->", color=c, lw=1.6))
    ax.text(cx + 0.115, 0.22, f"≈ {lam} nm", fontsize=10.5, color=c,
            ha="left", va="center")
ax.text(0.5, 0.86, "半导体量子点：「三维箱子」里的人造原子",
        ha="center", fontsize=13, color=INK, fontweight="bold")
ax.text(0.5, 0.06, "尺寸越小，能级间距越大，发光越偏蓝——2023 年诺贝尔化学奖",
        ha="center", fontsize=11, color=GRAY)
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_extra.png")
