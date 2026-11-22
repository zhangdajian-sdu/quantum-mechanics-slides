"""ch1-s4 §1.5 德布罗意物质波 — 全部插图（可重复运行）"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot

setup_plot()

import numpy as np
import matplotlib.pyplot as plt

INK = "#20242B"
TEAL = "#1F4E5F"
OCHRE = "#C4622D"
GRAY = "#8A8F98"
PAPER = "#FAF8F4"
PANEL = "#F3F1EA"
DARK = "#15181D"

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)


def save(fig, name, face=PAPER):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", facecolor=face)
    plt.close(fig)


# ---------- fig_cover.png  封面题图：玻尔轨道上的驻波（竖版） ----------
fig, ax = plt.subplots(figsize=(5.2, 8.2))
fig.patch.set_facecolor(PAPER)
ax.set_xlim(-6, 6); ax.set_ylim(-7.5, 6.5)
ax.set_aspect("equal"); ax.axis("off")

t = np.linspace(0, 2 * np.pi, 1200)
R = 3.4
n = 4
# 基圆轨道
ax.plot(R * np.cos(t), R * np.sin(t), color=GRAY, lw=1.4, ls="--")
# 驻波：径向正弦调制，整数 n 个波长恰好闭合
wave = (R + 0.55 * np.sin(n * t))
ax.plot(wave * np.cos(t), wave * np.sin(t), color=TEAL, lw=2.8)
# 核
ax.add_patch(plt.Circle((0, 0), 0.42, color=OCHRE, zorder=5))
# 反例：非整数波长不能闭合（下方小图）
R2 = 1.8
cy = -6.1
n2 = 3.5
ax.plot(R2 * np.cos(t) , cy + R2 * np.sin(t), color=GRAY, lw=1.0, ls="--")
w2 = R2 + 0.38 * np.sin(n2 * t)
ax.plot(w2 * np.cos(t), cy + w2 * np.sin(t), color=OCHRE, lw=2.0, alpha=0.9)
ax.text(0, 5.6, r"$2\pi r=n\lambda$", fontsize=17, color=INK, ha="center")
ax.text(0, 4.7, "整数个波长恰好闭合：允许的轨道", fontsize=11.5, color=GRAY, ha="center")
ax.text(0, cy - R2 - 0.75, "非整数波长自相抵消：轨道不允许", fontsize=11.5, color=GRAY, ha="center")
ax.set_ylim(-8.6, 6.5)
save(fig, "fig_cover.png")


# ---------- fig_rings.png  电子衍射环（深色底，现象引入） ----------
rng = np.random.default_rng(7)
fig, ax = plt.subplots(figsize=(6.4, 4.6))
fig.patch.set_facecolor(DARK)
ax.set_facecolor(DARK)
ax.set_xlim(-5, 5); ax.set_ylim(-3.6, 3.6)
ax.set_aspect("equal"); ax.axis("off")
# 中心亮斑 + 两层衍射环上的随机曝光点
radii = [(0.0, 0.16, 900), (1.35, 0.10, 520), (2.55, 0.12, 300)]
for r0, dr, cnt in radii:
    if r0 == 0.0:
        xs = rng.normal(0, dr * 1.6, cnt); ys = rng.normal(0, dr * 1.6, cnt)
    else:
        ang = rng.uniform(0, 2 * np.pi, cnt)
        rr = rng.normal(r0, dr, cnt)
        xs, ys = rr * np.cos(ang), rr * np.sin(ang)
    ax.scatter(xs, ys, s=rng.uniform(1, 7, cnt), c="#E8E4DA",
               alpha=rng.uniform(0.25, 0.95, cnt), lw=0)
for r0 in (1.35, 2.55):
    ax.add_patch(plt.Circle((0, 0), r0, fill=False, color="#8FA6B0",
                            lw=0.8, alpha=0.35))
ax.text(0, -3.25, "电子束穿过晶体后在屏上留下的环状图样（示意）",
        fontsize=11, color="#9AA3AB", ha="center")
save(fig, "fig_rings.png", face=DARK)


# ---------- fig_lambda.png  德布罗意波长的尺度对比（对数坐标） ----------
fig, ax = plt.subplots(figsize=(6.6, 3.4))
fig.patch.set_facecolor(PAPER)
items = [
    ("尘埃（教材例）", 6.6e-14, OCHRE),
    ("子弹  v=500 m/s", 1.3e-34, GRAY),
    ("电子  V=100 伏", 1.2e-8, TEAL),
    ("原子间距（晶格）", 2.0e-8, TEAL),
    ("电子直径上限", 1.0e-13, GRAY),
]
ys = np.arange(len(items))[::-1]
for (label, val, c), y in zip(items, ys):
    ax.scatter([val], [y], s=120, color=c, zorder=5)
    ax.text(val * 2.2, y, label, fontsize=11.5, color=INK, va="center")
ax.set_xscale("log")
ax.set_xlim(1e-36, 1e-4)
ax.set_ylim(-0.8, len(items) - 0.2)
ax.set_yticks([])
ax.set_xlabel("德布罗意波长  λ（厘米，对数刻度）", fontsize=11.5, color=INK)
ax.tick_params(axis="x", labelsize=10, colors=INK)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRAY)
# 可观测窗口：波长 ≥ 晶格间距才能被晶体衍射「看见」
ax.axvspan(1e-9, 1e-4, color=TEAL, alpha=0.06)
ax.text(3e-7, len(items) - 0.55, "≳ 晶格间距：波动可观测", fontsize=10.5,
        color=TEAL, ha="left")
save(fig, "fig_lambda.png")


# ---------- fig_davisson.png  戴维逊–革末实验示意 ----------
fig, ax = plt.subplots(figsize=(6.6, 4.4))
fig.patch.set_facecolor(PAPER)
ax.set_xlim(0, 12); ax.set_ylim(0, 8)
ax.set_aspect("equal"); ax.axis("off")
# 镍单晶表面（底部一排原子）
xsurf = np.linspace(2.2, 9.8, 9)
ax.plot([1.6, 10.4], [2.0, 2.0], color=INK, lw=2.2)
for x in xsurf:
    ax.add_patch(plt.Circle((x, 1.7), 0.26, color=TEAL, zorder=4))
ax.text(10.6, 1.7, "镍单晶", fontsize=11.5, color=INK, va="center")
ax.annotate("", xy=(4.2, 0.9), xytext=(2.4, 0.9),
            arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.4))
ax.text(3.3, 0.45, "d = 2.15 Å", fontsize=11, color=GRAY, ha="center")
# 入射电子束（竖直向下，正入射）
ax.annotate("", xy=(6.0, 2.3), xytext=(6.0, 6.9),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.4,
                            mutation_scale=18))
ax.text(6.25, 6.4, "电子束  V = 54 伏", fontsize=11.5, color=INK)
# 散射束：50° 方向
theta = np.deg2rad(50)
x1 = 6.0 - 4.4 * np.sin(theta); y1 = 2.0 + 4.4 * np.cos(theta)
ax.annotate("", xy=(x1, y1), xytext=(6.0, 2.3),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.4,
                            mutation_scale=18))
ax.add_patch(plt.Circle((x1 - 0.25, y1 + 0.18), 0.34, fill=False,
                        color=INK, lw=1.8))
ax.text(x1 - 1.35, y1 + 0.55, "探测器", fontsize=11.5, color=INK)
# 角度标注（入射方向的反向延长线与散射束夹角 50°）
arc = plt.matplotlib.patches.Arc((6.0, 2.0), 2.6, 2.6, angle=0,
                                 theta1=90, theta2=140, color=GRAY, lw=1.4)
ax.add_patch(arc)
ax.text(4.75, 3.75, r"$\theta=50^\circ$", fontsize=12, color=GRAY)
ax.text(6.0, 7.5, "在 θ=50° 方向出现第一级极强：nλ = d sinθ",
        fontsize=12, color=OCHRE, ha="center")
save(fig, "fig_davisson.png")


# ---------- fig_doubleslit.png  电子双缝干涉 ----------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 3.3),
                               gridspec_kw={"width_ratios": [1.25, 1]})
fig.patch.set_facecolor(PAPER)
# 左：装置示意
ax1.set_xlim(0, 10); ax1.set_ylim(0, 7)
ax1.axis("off")
ax1.annotate("", xy=(2.6, 3.5), xytext=(0.4, 3.5),
             arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.0))
ax1.text(0.4, 4.0, "电子枪", fontsize=11, color=INK)
ax1.plot([3.2, 3.2], [0.8, 6.2], color=INK, lw=2.2)
for yc in (2.6, 4.4):
    ax1.add_patch(plt.Rectangle((3.0, yc - 0.35), 0.4, 0.7, color=PAPER))
    ax1.plot([3.2, 3.2], [yc - 0.35, yc - 0.35], color=PAPER)
ax1.add_patch(plt.Rectangle((3.06, 2.25), 0.28, 0.7, color=PAPER, zorder=3))
ax1.add_patch(plt.Rectangle((3.06, 4.05), 0.28, 0.7, color=PAPER, zorder=3))
ax1.text(3.6, 5.6, "双缝", fontsize=11, color=INK)
# 两列球面波（只画缝右半平面）
t = np.linspace(-np.pi / 2, np.pi / 2, 200)
for r in np.arange(0.7, 5.6, 0.7):
    for yc in (2.6, 4.4):
        ax1.plot(3.2 + r * np.cos(t), yc + r * np.sin(t),
                 color=TEAL, lw=0.7, alpha=0.45)
ax1.plot([8.6, 8.6], [0.8, 6.2], color=INK, lw=2.6)
ax1.text(8.6, 6.5, "探测屏", fontsize=11, color=INK, ha="center")
# 右：干涉条纹强度
x = np.linspace(-3, 3, 600)
inten = np.cos(2.4 * x) ** 2 * np.sinc(x / 3.4) ** 2
ax2.fill_between(x, 0, inten, color=TEAL, alpha=0.85)
ax2.set_xticks([]); ax2.set_yticks([])
ax2.set_xlabel("屏上位置", fontsize=11, color=INK)
ax2.set_ylabel("电子计数", fontsize=11, color=INK)
for s in ("top", "right"):
    ax2.spines[s].set_visible(False)
ax2.spines["left"].set_color(GRAY); ax2.spines["bottom"].set_color(GRAY)
fig.subplots_adjust(wspace=0.25)
save(fig, "fig_doubleslit.png")

print("done: 5 figures ->", OUT)
