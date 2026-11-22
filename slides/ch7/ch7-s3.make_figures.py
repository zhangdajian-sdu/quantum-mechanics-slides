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


# ---------- 封面：把上限压到最低（teal 底） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

x = np.linspace(0.08, 0.92, 200)
E = 1.2 * (x - 0.5) ** 2 + 1.75
ax.plot(x, E, color="#FAF8F4", lw=2.8, solid_capstyle="round")
ax.plot([0.5], [1.75], "o", ms=10, color="#E8B48C", zorder=5)
ax.plot([0.14, 0.86], [1.52, 1.52], color="#E8B48C", lw=2.0, ls=(0, (6, 4)))
ax.annotate("", xy=(0.68, 1.56), xytext=(0.68, 1.71),
            arrowprops=dict(arrowstyle="<->", color="#FFFFFFAA", lw=1.3))
ax.text(0.72, 1.60, "永远差一点儿", color="#FFFFFFAA", fontsize=11.5, va="center")
ax.text(0.5, 1.92, "试探波函数族的能量曲线", color="#FAF8F4", fontsize=13, ha="center")
ax.text(0.5, 2.62, "把上限压到最低", color="#FAF8F4", fontsize=17, ha="center", weight="bold")
ax.text(0.86, 1.38, r"$E_0$（真基态）", color="#E8B48C", fontsize=13, ha="right")
ax.text(0.08, 1.06, "最低点 = 最好的近似", color="#FFFFFF99", fontsize=12.5, ha="left")
ax.set_xlim(0, 1); ax.set_ylim(0.9, 3.0)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 引入：三个猜测，三个上限 ----------
fig, ax = plt.subplots(figsize=(8.4, 5.6), facecolor=PAPER)
ax.set_facecolor(PAPER)

E0 = 1.0
xs = [0.25, 0.50, 0.75]
tops = [2.30, 1.70, 2.00]
labels = [r"$E[\psi_1]$", r"$E[\psi_2]$", r"$E[\psi_3]$"]
cols = [GRAY, OCHRE, GRAY]
ax.plot([0.06, 0.94], [E0, E0], color=INK, lw=2.2, ls=(0, (6, 4)))
ax.text(0.94, E0 - 0.16, r"$E_0$（真基态能量）", ha="right", fontsize=12, color=INK)
for x, t, lb, c in zip(xs, tops, labels, cols):
    ax.plot([x, x], [E0, t], color=c, lw=3.0, solid_capstyle="round")
    ax.plot([x], [t], "o", ms=8, color=c)
    ax.text(x, t + 0.10, lb, ha="center", fontsize=13, color=c)
ax.annotate("", xy=(0.50, 1.06), xytext=(0.50, 1.64),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.4))
ax.text(0.56, 1.32, "最低的获胜", fontsize=12, color=OCHRE)
ax.set_xlim(0, 1); ax.set_ylim(0.6, 2.7)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title("任意猜测给出的平均能量，都在真基态能量上方", fontsize=13.5, color=INK, pad=8)
save(fig, "fig_trial.png")


# ---------- 例题：氦原子 E(Z) 曲线 ----------
fig, ax = plt.subplots(figsize=(8.4, 5.4), facecolor=PAPER)
ax.set_facecolor(PAPER)

Z = np.linspace(1.2, 2.2, 200)
EZ = Z ** 2 - 27 * Z / 8
ax.plot(Z, EZ, color=TEAL, lw=2.6)
Zmin = 27 / 16
ax.plot([Zmin], [Zmin ** 2 - 27 * Zmin / 8], "o", ms=9, color=OCHRE, zorder=5)
ax.annotate(r"$Z=27/16\approx1.69$，$E\approx-2.85\,e^2/a$",
            xy=(Zmin, -2.85), xytext=(1.32, -2.66),
            fontsize=12, color=OCHRE,
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.4))
ax.plot([1.2, 2.2], [-2.904, -2.904], color=GRAY, lw=1.8, ls=(0, (6, 4)))
ax.text(2.2, -2.935, r"实验值 $-2.904\,e^2/a$", ha="right", fontsize=11.5, color=GRAY)
ax.plot([2.0], [4 - 27 * 2 / 8], "o", ms=7, color=INK, zorder=5)
ax.annotate(r"$Z=2$（不屏蔽）：$-2.75$", xy=(2.0, -2.75), xytext=(1.82, -2.60),
            fontsize=11.5, color=INK,
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2))
ax.set_xlabel(r"有效电荷 $Z$", fontsize=12.5, color=INK)
ax.set_ylabel(r"$E(Z)$（单位 $e^2/a$）", fontsize=12.5, color=INK)
ax.set_xlim(1.2, 2.2); ax.set_ylim(-3.0, -2.4)
ax.tick_params(colors=GRAY, labelsize=10)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(HAIR)
ax.set_title(r"氦原子基态：$E(Z)=Z^2-\dfrac{27}{8}Z$（单位 $e^2/a$）", fontsize=13.5, color=INK, pad=8)
save(fig, "fig_ez.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
