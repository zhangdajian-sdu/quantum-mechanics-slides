"""ch1-s2 §1.3 光电效应与光量子 — 全部插图（可重复运行）"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot

setup_plot()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle, Arc

INK = "#20242B"
TEAL = "#1F4E5F"
OCHRE = "#C4622D"
GRAY = "#8A8F98"
PAPER = "#FAF8F4"
PANEL = "#F3F1EA"

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", facecolor=PAPER)
    plt.close(fig)


# ---------- fig_cover.png  封面题图：T_max–nu 直线 ----------
fig, ax = plt.subplots(figsize=(5.2, 8.2))
fig.patch.set_facecolor(PAPER)
nu = np.linspace(0, 10, 200)
nu0 = 4.0
T = np.maximum(nu - nu0, 0)
ax.axvspan(0, nu0, color=PANEL, zorder=0)
ax.plot(nu, T, color=OCHRE, lw=3.2, zorder=3)
rng = np.random.default_rng(7)
nud = rng.uniform(4.6, 9.4, 14)
ax.scatter(nud, nud - nu0 + rng.normal(0, 0.16, len(nud)),
           s=26, color=TEAL, zorder=4, edgecolors="none")
ax.axhline(0, color=GRAY, lw=1.0)
ax.plot([nu0], [0], marker="o", ms=8, color=INK, zorder=5)
ax.annotate(r"$\nu_0=A/h$", xy=(nu0, 0), xytext=(nu0 - 0.5, 1.1),
            fontsize=15, color=INK)
ax.annotate(r"$\mathrm{slope}=h$", xy=(7.6, 3.6), xytext=(5.6, 4.6),
            fontsize=15, color=OCHRE,
            arrowprops=dict(arrowstyle="->", color=OCHRE, lw=1.4))
ax.text(1.9, 4.4, "无\n光\n电\n子", fontsize=15, color=GRAY,
        ha="center", va="center", linespacing=1.5)
ax.set_xlabel(r"$\nu$", fontsize=15)
ax.set_ylabel(r"$T_{\max}$", fontsize=15)
ax.set_xlim(0, 10)
ax.set_ylim(-0.6, 6.2)
ax.set_xticks([]); ax.set_yticks([])
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(GRAY)
ax.tick_params(colors=GRAY)
ax.xaxis.label.set_color(INK); ax.yaxis.label.set_color(INK)
save(fig, "fig_cover.png")


# ---------- fig_setup.png  光电效应实验装置示意 ----------
fig, ax = plt.subplots(figsize=(7.2, 5.0))
fig.patch.set_facecolor(PAPER)
ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")

# 真空管
tube = Rectangle((1.2, 1.6), 6.2, 3.6, fill=True, facecolor="#FFFFFF",
                 edgecolor=INK, lw=1.6)
ax.add_patch(tube)
ax.text(4.3, 5.55, "真空管", fontsize=12.5, color=GRAY, ha="center")

# 阴极（金属板）与阳极
ax.add_patch(Rectangle((1.7, 2.2), 0.28, 2.4, facecolor=TEAL, edgecolor="none"))
ax.text(3.0, 2.42, "金属阴极", fontsize=10.5, color=INK, ha="center")
ax.add_patch(Rectangle((6.3, 2.9), 0.22, 1.0, facecolor=OCHRE, edgecolor="none"))
ax.text(6.41, 2.35, "阳极", fontsize=11.5, color=INK, ha="center")

# 入射光（波浪箭头射向阴极）
t = np.linspace(0, 1, 300)
for i, y0 in enumerate([4.35, 3.65]):
    x = -1.0 + 2.6 * t
    y = y0 + 0.14 * np.sin(2 * np.pi * 4.2 * t)
    ax.plot(x, y, color=OCHRE, lw=2.0)
    ax.annotate("", xy=(1.68, y0), xytext=(1.30, y0 + 0.14 * np.sin(2 * np.pi * 4.2)),
                arrowprops=dict(arrowstyle="->", color=OCHRE, lw=2.0))
ax.text(0.1, 4.75, r"入射光 $\nu$", fontsize=12.5, color=OCHRE)

# 光电子
for (x0, y0, x1, y1) in [(2.3, 4.2, 6.2, 4.35), (2.3, 3.4, 6.2, 3.3), (2.3, 2.7, 6.2, 2.75)]:
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.3, linestyle=(0, (4, 3))))
ax.text(4.1, 4.62, r"光电子 $e^-$", fontsize=12, color=TEAL, ha="center")

# 外电路：电流计 + 电源
ax.plot([1.84, 1.84, 3.6], [2.2, 0.9, 0.9], color=INK, lw=1.4)
ax.plot([4.9, 6.41, 6.41], [0.9, 0.9, 2.2], color=INK, lw=1.4)
circ = Circle((4.25, 0.9), 0.62, fill=True, facecolor=PAPER, edgecolor=INK, lw=1.4)
ax.add_patch(circ)
ax.text(4.25, 0.9, "G", fontsize=15, color=INK, ha="center", va="center")
ax.text(4.25, 0.02, "光电流", fontsize=11, color=GRAY, ha="center")
save(fig, "fig_setup.png")


# ---------- fig_tmax.png  T_max-nu 实验直线 ----------
fig, ax = plt.subplots(figsize=(6.6, 4.6))
fig.patch.set_facecolor(PAPER)
nu = np.linspace(0, 12, 300)
nu0 = 5.0
hline = 1.0
T = np.maximum(hline * (nu - nu0), 0)
ax.plot(nu, T, color=OCHRE, lw=2.6, zorder=3, label=r"$T_{\max}=h\nu-A$")
nud = np.array([5.6, 6.3, 7.0, 7.8, 8.5, 9.2, 10.1, 10.9])
rng = np.random.default_rng(3)
ax.scatter(nud, hline * (nud - nu0) + rng.normal(0, 0.12, len(nud)),
           s=34, color=TEAL, zorder=4, edgecolors="white", linewidths=0.6,
           label="实验点")
ax.plot([nu0], [0], marker="o", ms=7, color=INK, zorder=5)
ax.annotate(r"临界频率 $\nu_0=A/h$", xy=(nu0, 0), xytext=(2.1, 1.5),
            fontsize=12.5, color=INK,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.1))
# 斜率标注
ax.plot([7.0, 9.0, 9.0], [2.0, 2.0, 4.0], color=GRAY, lw=1.0, ls=":")
ax.text(8.0, 1.55, r"$\Delta\nu$", fontsize=12, color=GRAY, ha="center")
ax.text(9.15, 3.0, r"$\Delta T_{\max}$", fontsize=12, color=GRAY, va="center")
ax.text(5.0, 6.1, r"斜率 $\Delta T_{\max}/\Delta\nu=h$", fontsize=13,
        color=OCHRE)
ax.set_xlabel(r"频率 $\nu$", fontsize=12.5)
ax.set_ylabel(r"最大动能 $T_{\max}$", fontsize=12.5)
ax.set_xlim(0, 12); ax.set_ylim(-0.4, 7.6)
ax.set_xticks([]); ax.set_yticks([])
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(GRAY)
ax.tick_params(colors=GRAY)
ax.legend(loc="upper left", frameon=False, fontsize=11.5)
save(fig, "fig_tmax.png")


# ---------- fig_compton.png  康普顿散射几何 ----------
fig, ax = plt.subplots(figsize=(6.8, 4.6))
fig.patch.set_facecolor(PAPER)
ax.set_xlim(-0.5, 10); ax.set_ylim(-3.6, 4.2); ax.axis("off")

# 电子（碰撞点）
ec = Circle((4.6, 0), 0.34, facecolor=TEAL, edgecolor="none", zorder=5)
ax.add_patch(ec)
ax.text(4.6, 0, r"$e^-$", fontsize=11, color="white", ha="center", va="center", zorder=6)
ax.text(3.1, -1.0, "电子（视为自由、静止）", fontsize=10.5, color=GRAY, ha="center")

# 入射光子
ax.annotate("", xy=(4.15, 0), xytext=(0.4, 0),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.6, mutation_scale=22))
ax.text(1.9, 0.62, r"入射光子  $E_0=h\nu_0,\ \boldsymbol{p}_0=\dfrac{h}{\lambda_0}\boldsymbol{k}$",
        fontsize=12.5, color=OCHRE, ha="center")

# 散射光子（theta 方向）
th = np.deg2rad(38)
ax.annotate("", xy=(4.6 + 4.6 * np.cos(th), 4.6 * np.sin(th)), xytext=(4.85, 0.12),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.6, mutation_scale=22))
ax.text(7.6, 2.9, r"散射光子  $E=h\nu,\ \boldsymbol{p}=\dfrac{h}{\lambda}\boldsymbol{n}$",
        fontsize=12.5, color=OCHRE, ha="center")

# 反冲电子
ph = np.deg2rad(-30)
ax.annotate("", xy=(4.6 + 3.3 * np.cos(ph), 3.3 * np.sin(ph)), xytext=(4.9, -0.12),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.6, mutation_scale=22))
ax.text(7.3, -2.15, r"反冲电子  $\boldsymbol{p}_e$", fontsize=12.5, color=TEAL, ha="center")

# 角度标注
arc1 = Arc((4.6, 0), 3.4, 3.4, angle=0, theta1=0, theta2=38, color=INK, lw=1.2)
ax.add_patch(arc1)
ax.text(6.6, 0.55, r"$\theta$", fontsize=13, color=INK)
ax.plot([4.6, 9.4], [0, 0], color=GRAY, lw=0.9, ls=(0, (4, 3)))
save(fig, "fig_compton.png")


# ---------- fig_cv.png  固体比热（爱因斯坦模型） ----------
fig, ax = plt.subplots(figsize=(6.6, 4.4))
fig.patch.set_facecolor(PAPER)
TT = np.linspace(0.04, 3.0, 400)          # T / theta_E
x = 1.0 / TT                               # h nu / kT
C = 3 * x**2 * np.exp(x) / (np.exp(x) - 1) ** 2
ax.plot(TT, C, color=TEAL, lw=2.8, zorder=3)
ax.axhline(3, color=GRAY, lw=1.2, ls="--")
ax.text(2.62, 3.08, "经典值 $3k$", fontsize=12, color=GRAY)
ax.annotate("高温 $kT\\gg h\\nu$：$C\\to 3k$", xy=(2.4, 2.97), xytext=(1.15, 2.35),
            fontsize=12, color=INK,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.1))
ax.annotate("低温 $kT\\ll h\\nu$：$C\\to 0$", xy=(0.16, 0.35), xytext=(0.6, 1.15),
            fontsize=12, color=INK,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.1))
ax.set_xlabel(r"温度 $T$（以 $h\nu/k$ 为单位）", fontsize=12.5)
ax.set_ylabel(r"原子比热 $C$（以 $k$ 为单位）", fontsize=12.5)
ax.set_xlim(0, 3.0); ax.set_ylim(0, 3.5)
ax.set_xticks([]); ax.set_yticks([3])
ax.set_yticklabels(["$3k$"], fontsize=11)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(GRAY)
ax.tick_params(colors=GRAY)
save(fig, "fig_cv.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
