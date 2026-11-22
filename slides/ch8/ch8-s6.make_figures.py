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
HAIR = "#E2DFD8"

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print("saved", name)


# ---------- 封面：磁场中谱线一分为三（teal 底） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

ax.text(0.0, 2.62, "加磁场 $\\boldsymbol{B}$，", color="#FAF8F4", fontsize=18,
        ha="center", weight="bold")
ax.text(0.0, 2.36, "谱线裂成三条", color="#FAF8F4", fontsize=18,
        ha="center", weight="bold")

# 磁铁 N/S
ax.add_patch(plt.Rectangle((-3.0, 1.52), 1.0, 0.44, color="#FFFFFF22"))
ax.add_patch(plt.Rectangle((2.0, 1.52), 1.0, 0.44, color="#FFFFFF22"))
ax.text(-2.5, 1.74, "N", color="#FAF8F4", fontsize=14, ha="center", va="center",
        weight="bold")
ax.text(2.5, 1.74, "S", color="#FAF8F4", fontsize=14, ha="center", va="center",
        weight="bold")
for yy in (1.62, 1.74, 1.86):
    ax.annotate("", xy=(1.85, yy), xytext=(-1.85, yy),
                arrowprops=dict(arrowstyle="-|>", color="#FFFFFF55", lw=1.2))
ax.text(0.0, 1.34, "$\\boldsymbol{B}$", color="#FAF8F4", fontsize=13, ha="center")

# 上：无场 一条谱线
ax.plot([-2.9, -1.4], [0.62, 0.62], color="#FFFFFF55", lw=1.0)
ax.plot([-2.15], [0.98], marker="|", ms=44, color="#FFFFFFAA", mew=2.4)
ax.text(-2.15, 0.28, "无磁场：一条", color="#FFFFFF88", fontsize=10.5, ha="center")

ax.annotate("", xy=(-0.35, 0.8), xytext=(-1.2, 0.8),
            arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=1.6))

# 右：三条
ax.plot([0.1, 2.7], [0.62, 0.62], color="#FFFFFF55", lw=1.0)
for x, c in ((1.02, "#E8B48C"), (1.40, "#FAF8F4"), (1.78, "#E8B48C")):
    ax.plot([x], [0.98], marker="|", ms=44, color=c, mew=2.4)
ax.text(1.40, 0.28, "强场：三条（正常塞曼）", color="#FAF8F4", fontsize=10.5,
        ha="center")

# 下：弱场 多条
ax.plot([-2.9, -1.4], [-0.85, -0.85], color="#FFFFFF55", lw=1.0)
ax.plot([-2.15], [-0.49], marker="|", ms=44, color="#FFFFFFAA", mew=2.4)
ax.text(-2.15, -1.19, "无磁场：一条", color="#FFFFFF88", fontsize=10.5, ha="center")

ax.annotate("", xy=(-0.35, -0.67), xytext=(-1.2, -0.67),
            arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=1.6))

ax.plot([0.1, 2.7], [-0.85, -0.85], color="#FFFFFF55", lw=1.0)
for x in (0.72, 1.02, 1.26, 1.54, 1.78, 2.08):
    ax.plot([x], [-0.49], marker="|", ms=44, color="#E8B48C", mew=2.2)
ax.text(1.40, -1.19, "弱场：更多条（反常塞曼）", color="#FAF8F4", fontsize=10.5,
        ha="center")

ax.text(0.0, -1.86, "判据：$B$ 项与自旋–轨道耦合 $\\xi(r)\\hat{\\boldsymbol{S}}\\cdot\\hat{\\boldsymbol{L}}$ 谁大",
        color="#FAF8F4", fontsize=11.5, ha="center")
ax.text(0.0, -2.2, "强场略去耦合 → 正常；弱场留着耦合 → 反常",
        color="#FFFFFF99", fontsize=10.5, ha="center")

ax.set_xlim(-3.4, 3.4)
ax.set_ylim(-2.5, 2.95)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 正常塞曼：3p -> 3s（paper 底） ----------
fig, ax = plt.subplots(figsize=(7.4, 4.9), facecolor=PAPER)
ax.set_facecolor(PAPER)

xp = {-2: 0.6, -1: 1.7, 0: 2.8, 1: 3.9, 2: 5.0}
yp = 3.3
ys = 0.7
xs = {-1: 2.2, 1: 3.4}

# 3p 五条
for sh, x in xp.items():
    ax.plot([x - 0.42, x + 0.42], [yp, yp], color=INK, lw=2.2)
    ax.text(x, yp + 0.13, f"{sh:+d}" if sh != 0 else "0", color=INK, fontsize=10,
            ha="center")
ax.text(0.6, yp + 0.44, "$3p$：$m+2m_s=-2,-1,0,0,+1,+2$ → 5 条", color=INK,
        fontsize=10.5, ha="left")
ax.text(5.55, yp, "等间距 $\\Delta E$", color=GRAY, fontsize=10, ha="left",
        va="center")

# 3s 两条
for sh, x in xs.items():
    ax.plot([x - 0.42, x + 0.42], [ys, ys], color=INK, lw=2.2)
    ax.text(x + 0.56, ys, f"{sh:+d}", color=INK, fontsize=10, ha="left",
            va="center")
ax.text(0.6, ys - 0.30, "$3s$：$m_s=\\pm\\frac{1}{2}$ → 2 条", color=INK,
        fontsize=10.5, ha="left")
ax.text(5.55, ys, "间距 $2\\Delta E$", color=GRAY, fontsize=10, ha="left",
        va="center")

# 允许跃迁（Δms=0）：六条，三种频率
# ms=+1/2: p(0)@2.8 -> s(+1)@3.4 频移-1; p(1)@3.9 -> s(+1) 频移0; p(2)@5.0 -> s(+1) 频移+1
# ms=-1/2: p(-2)@0.6 -> s(-1)@2.2 频移-1; p(-1)@1.7 -> s(-1) 频移0; p(0)@2.8 -> s(-1) 频移+1
C = {-1: TEAL, 0: OCHRE, 1: TEAL}
for x_from, x_to, nu in ((2.8, 3.4, -1), (3.9, 3.4, 0), (5.0, 3.4, 1),
                         (0.6, 2.2, -1), (1.7, 2.2, 0), (2.8, 2.2, 1)):
    ax.annotate("", xy=(x_to, ys + 0.06), xytext=(x_from, yp - 0.06),
                arrowprops=dict(arrowstyle="-|>", color=C[nu], lw=1.3,
                                shrinkA=0, shrinkB=0, alpha=0.85))

# 谱线：三条
ysp = -0.55
ax.plot([1.1, 5.2], [ysp, ysp], color=HAIR, lw=1.2)
for x, c, lab in ((2.2, TEAL, "$\\omega_0-\\Delta\\omega$"),
                  (3.15, OCHRE, "$\\omega_0$"),
                  (4.1, TEAL, "$\\omega_0+\\Delta\\omega$")):
    ax.plot([x], [ysp + 0.34], marker="|", ms=40, color=c, mew=2.6)
    ax.text(x, ysp - 0.30, lab, color=INK, fontsize=9.5, ha="center")
ax.text(0.6, ysp + 0.28, "谱线", color=GRAY, fontsize=10, ha="left", va="center")
ax.text(5.45, ysp + 0.28, "6 对跃迁\n只有 3 种频率", color=GRAY, fontsize=9.5,
        ha="left", va="center")

ax.set_xlim(0, 7.2)
ax.set_ylim(-1.15, 4.05)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_normal.png")


# ---------- 反常塞曼：钠 D 线弱场分裂（paper 底） ----------
fig, ax = plt.subplots(figsize=(7.4, 5.0), facecolor=PAPER)
ax.set_facecolor(PAPER)

# --- 左：能级 ---
# 3P3/2: g=4/3, mj=±1/2,±3/2 -> g*mj = ±2/3, ±2
lv = {(-2.0, "P32"): (0.6, 3.62), (-2 / 3, "P32"): (0.6, 3.30),
      (2 / 3, "P32"): (0.6, 2.98), (2.0, "P32"): (0.6, 2.66)}
y0 = 3.14
for gm, x in ((-2.0, 0.6), (-2 / 3, 0.6), (2 / 3, 0.6), (2.0, 0.6)):
    y = y0 + gm * 0.16
    ax.plot([x, x + 1.3], [y, y], color=TEAL, lw=2.0)
ax.text(1.25, 3.62, "$3\\,{}^2P_{3/2}$，$g=\\frac{4}{3}$", color=TEAL,
        fontsize=10.5, ha="center")

y0 = 2.10
for gm in (-1 / 3, 1 / 3):
    y = y0 + gm * 0.3
    ax.plot([0.6, 1.9], [y, y], color=OCHRE, lw=2.0)
ax.text(1.25, 2.34, "$3\\,{}^2P_{1/2}$，$g=\\frac{2}{3}$", color=OCHRE,
        fontsize=10.5, ha="center")

y0 = 0.78
for gm in (-1.0, 1.0):
    y = y0 + gm * 0.16
    ax.plot([0.6, 1.9], [y, y], color=INK, lw=2.0)
ax.text(1.25, 0.40, "$3\\,{}^2S_{1/2}$，$g=2$", color=INK, fontsize=10.5,
        ha="center")
ax.text(1.25, 4.02, "弱场中的能级（间距被夸大）", color=GRAY, fontsize=9.5,
        ha="center")

# --- 右：谱线棒图 ---
ax.plot([2.6, 2.6], [0.3, 4.0], color=HAIR, lw=1.0)

u = 0.30  # 单位位移的像素宽
xc = 4.9

# D2: 6 条 ±1/3, ±1, ±5/3
y = 3.35
ax.plot([3.1, 6.7], [y - 0.42, y - 0.42], color=HAIR, lw=1.0)
for d in (-5 / 3, -1, -1 / 3, 1 / 3, 1, 5 / 3):
    ax.plot([xc + d * u * 2], [y], marker="|", ms=34, color=TEAL, mew=2.4)
ax.plot([xc], [y], marker="|", ms=34, color=TEAL, mew=0, alpha=0)
ax.text(2.9, y + 0.02, "$D_2$", color=TEAL, fontsize=11, ha="right", va="center")
ax.text(xc, y + 0.34, "6 条：$\\pm\\frac{1}{3},\\ \\pm1,\\ \\pm\\frac{5}{3}$",
        color=GRAY, fontsize=9.5, ha="center",
        bbox=dict(boxstyle="square,pad=0.25", fc=PAPER, ec="none"))

# D1: 4 条 ±2/3, ±4/3
y = 2.15
ax.plot([3.1, 6.7], [y - 0.42, y - 0.42], color=HAIR, lw=1.0)
for d in (-4 / 3, -2 / 3, 2 / 3, 4 / 3):
    ax.plot([xc + d * u * 2], [y], marker="|", ms=34, color=OCHRE, mew=2.4)
ax.text(2.9, y + 0.02, "$D_1$", color=OCHRE, fontsize=11, ha="right", va="center")
ax.text(xc, y + 0.34, "4 条：$\\pm\\frac{2}{3},\\ \\pm\\frac{4}{3}$",
        color=GRAY, fontsize=9.5, ha="center",
        bbox=dict(boxstyle="square,pad=0.25", fc=PAPER, ec="none"))

# 原频率虚线
ax.plot([xc, xc], [1.55, 3.8], color=GRAY, lw=1.0, ls=(0, (4, 3)))
ax.text(xc, 1.32, "$\\omega_0$（无场位置）", color=GRAY, fontsize=9.5,
        ha="center")
ax.text(xc, 0.92, "横轴：频率位移，单位 $\\frac{eB\\hbar}{2\\mu c}$",
        color=INK, fontsize=10, ha="center")
ax.text(4.9, 4.02, "谱线分裂（反常塞曼）", color=GRAY, fontsize=9.5, ha="center")

ax.set_xlim(0, 7.2)
ax.set_ylim(0.55, 4.25)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_anomalous.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
