"""第五章 §5.4 插图：封面题图（右矢/左矢/内积）+ 引入页示意图（一个态，三种面貌）"""
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
LIGHT = "#DCE6EA"
PANEL_TEAL = "#23586B"

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)

# ---------- 封面题图：|ψ⟩ 与 ⟨φ|ψ⟩ ----------
fig, ax = plt.subplots(
    figsize=(5.2, 6.2),
)
fig.patch.set_facecolor(PANEL_TEAL)
ax.set_facecolor(PANEL_TEAL)
fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)

# 上方：一个大右矢包住态矢箭头（| 在左，ψ 箭头居中，⟩ 在右）
ax.annotate("", xy=(0.42, 2.05), xytext=(-0.32, 0.5),
            arrowprops=dict(arrowstyle="-|>", color="#FFFFFF", lw=3.0))
ax.text(0.52, 2.0, r"$\psi$", color="#FFFFFF", fontsize=20)
ax.text(-0.75, 1.0, r"$|$", color=OCHRE, fontsize=120, ha="center", va="center")
ax.text(0.85, 1.0, r"$\rangle$", color=OCHRE, fontsize=60, ha="center", va="center")
ax.text(0, -0.05, "态矢本身：不指名表象", color="#FFFFFFCC", fontsize=14, ha="center")

# 中间分隔
ax.plot([-1.7, 1.7], [-0.75, -0.75], color="#FFFFFF2E", lw=1)

# 下方：左矢+右矢=内积（一个数）
ax.text(0, -1.6, r"$\langle\varphi\,|\,\psi\rangle$", color="#FFFFFF",
        fontsize=34, ha="center", va="center")
ax.text(0, -2.35, "内积：一个不依赖表象的数", color="#FFFFFFCC", fontsize=14, ha="center")

ax.set_xlim(-1.9, 1.9)
ax.set_ylim(-2.9, 2.9)
ax.set_aspect("equal")
ax.axis("off")
fig.savefig(OUT / "fig_cover.png", dpi=220, facecolor=PANEL_TEAL)
plt.close(fig)

# ---------- 引入页：一个 |ψ⟩，三种表象三种读数 ----------
fig, ax = plt.subplots(figsize=(7.2, 4.8))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

# 中心节点
c = plt.Circle((0, 0), 0.42, color=TEAL, zorder=3)
ax.add_patch(c)
ax.text(0, 0, r"$|\psi\rangle$", color="#FFFFFF", fontsize=16,
        ha="center", va="center", zorder=4)

# 三个分支
def branch(angle_deg, box_xy, title, draw, title_pos=None):
    a = np.deg2rad(angle_deg)
    end = np.array([1.15 * np.cos(a), 1.15 * np.sin(a)])
    ax.annotate("", xy=end, xytext=(0.48 * np.cos(a), 0.48 * np.sin(a)),
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.6))
    draw(box_xy)
    if title_pos is None:
        title_pos = (box_xy[0], box_xy[1] - 0.98, "center")
    ax.text(title_pos[0], title_pos[1], title, fontsize=12.5, color=INK,
            ha=title_pos[2], va="top")

def draw_col(xy):
    x0, y0 = xy
    for i, h in enumerate([0.30, 0.48, 0.38]):
        r = plt.Rectangle((x0 - 0.18, y0 - 0.5 + i * 0.36), 0.36, h,
                          facecolor=LIGHT, edgecolor=TEAL, lw=1.2)
        ax.add_patch(r)

def draw_curve(xy, color, phase):
    x0, y0 = xy
    xs = np.linspace(-0.75, 0.75, 200)
    ys = 0.42 * np.exp(-(xs / 0.4) ** 2) * np.cos(3.2 * xs + phase)
    ax.plot(x0 + xs, y0 + ys, color=color, lw=1.8)
    ax.axhline(y0, color=GRAY, lw=0.8, zorder=1)

branch(90, (0, 2.0), "Q 表象：一列数 $\\{C_n\\}$", draw_col, title_pos=(0.18, 1.5, "left"))
branch(210, (-1.55, -1.15), "x 表象：曲线 $\\psi(x)$", lambda xy: draw_curve(xy, TEAL, 0))
branch(330, (1.55, -1.15), "p 表象：曲线 $\\varphi(p)$", lambda xy: draw_curve(xy, OCHRE, 1.2))

ax.set_xlim(-2.6, 2.6)
ax.set_ylim(-2.75, 2.75)
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout()
fig.savefig(OUT / "fig_intro.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ---------- 新引入页：同一态的三张「照片」 ----------
fig = plt.figure(figsize=(7.6, 4.9))
fig.patch.set_facecolor(PAPER)

xs = np.linspace(-3.2, 3.2, 400)

# 照片 1：x 表象波函数（振荡波包）
ax1 = fig.add_axes([0.05, 0.30, 0.26, 0.52])
ax1.set_facecolor(PAPER)
ax1.plot(xs, np.exp(-(xs / 1.5) ** 2) * np.cos(3.5 * xs), color=TEAL, lw=1.8)
ax1.axhline(0, color=GRAY, lw=0.8)
ax1.set_title("「照片」1：一条曲线", fontsize=12.5, color=INK, pad=8)
ax1.text(0, -1.35, r"$\psi(x)$", fontsize=15, color=TEAL, ha="center")
ax1.set_xlim(-3.2, 3.2)
ax1.set_ylim(-1.7, 1.25)
ax1.axis("off")

# 照片 2：p 表象波函数（另一条曲线）
ax2 = fig.add_axes([0.38, 0.30, 0.26, 0.52])
ax2.set_facecolor(PAPER)
ax2.plot(xs, np.exp(-(xs / 1.1) ** 2), color=OCHRE, lw=1.8)
ax2.axhline(0, color=GRAY, lw=0.8)
ax2.set_title("「照片」2：另一条曲线", fontsize=12.5, color=INK, pad=8)
ax2.text(0, -1.35, r"$\varphi(p)$", fontsize=15, color=OCHRE, ha="center")
ax2.set_xlim(-3.2, 3.2)
ax2.set_ylim(-1.7, 1.25)
ax2.axis("off")

# 照片 3：Q 表象的一列系数
ax3 = fig.add_axes([0.71, 0.30, 0.24, 0.52])
ax3.set_facecolor(PAPER)
for i, (h, lab) in enumerate([(0.42, "$C_1$"), (0.72, "$C_2$"),
                              (0.55, "$C_3$"), (0.30, "$C_4$")]):
    ax3.add_patch(plt.Rectangle((i * 0.9, 0), 0.55, h,
                                facecolor=LIGHT, edgecolor=TEAL, lw=1.2))
    ax3.text(i * 0.9 + 0.27, -0.28, lab, fontsize=11.5, color=INK, ha="center")
ax3.axhline(0, color=GRAY, lw=0.8)
ax3.set_title("「照片」3：一列复数", fontsize=12.5, color=INK, pad=8)
ax3.set_xlim(-0.3, 3.6)
ax3.set_ylim(-1.7, 1.25)
ax3.axis("off")

fig.text(0.5, 0.90, "同一个量子态，三张长得完全不同的「照片」",
         fontsize=14.5, color=INK, ha="center")
fig.text(0.5, 0.10, "它们是同一个对象——能不能给它一个不指名表象的名字？",
         fontsize=13, color=GRAY, ha="center")
fig.savefig(OUT / "fig_photos.png", dpi=200, facecolor=PAPER)
plt.close(fig)

print("done:", [p.name for p in OUT.glob("*.png")])
