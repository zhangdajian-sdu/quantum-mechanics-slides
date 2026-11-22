"""ch1-s3 §1.4 玻尔原子结构理论 — 全部插图（可重复运行）"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot

setup_plot()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

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


# ---------- fig_cover.png  封面题图：分立能级与跃迁 ----------
fig, ax = plt.subplots(figsize=(5.2, 8.2))
fig.patch.set_facecolor(PAPER)
ax.set_xlim(0, 10); ax.set_ylim(0, 14)
ax.axis("off")
levels = {1: 1.2, 2: 5.2, 3: 7.6, 4: 9.0, 5: 9.9}
for n, y in levels.items():
    ax.plot([1.2, 8.8], [y, y], color=TEAL, lw=3.0)
    ax.text(0.6, y, f"$n={n}$", fontsize=14, color=INK, va="center", ha="right")
ax.plot([1.2, 8.8], [11.6, 11.6], color=GRAY, lw=1.2, ls="--")
ax.text(0.6, 11.6, "$E=0$", fontsize=13, color=GRAY, va="center", ha="right")
for (y0, y1, x) in [(5.2, 1.2, 3.0), (7.6, 1.2, 5.0), (9.0, 5.2, 7.0)]:
    ax.annotate("", xy=(x, y1 + 0.15), xytext=(x, y0 - 0.15),
                arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.4,
                                mutation_scale=20))
ax.text(5.0, 13.2, r"$h\nu=E_n-E_m$", fontsize=16, color=OCHRE, ha="center")
save(fig, "fig_cover.png")


# ---------- fig_spectrum.png  氢原子巴耳末系谱线 ----------
# 可见区巴耳末系：Hα 656.3 红, Hβ 486.1 青, Hγ 434.0 蓝, Hδ 410.2 紫 (nm)
lines = [(656.3, "#D22B2B", r"H$\alpha$"), (486.1, "#2E8B9E", r"H$\beta$"),
         (434.0, "#3B4CC0", r"H$\gamma$"), (410.2, "#7A3FA0", r"H$\delta$")]
fig, ax = plt.subplots(figsize=(7.0, 3.4))
fig.patch.set_facecolor(PAPER)
ax.set_xlim(380, 680); ax.set_ylim(0, 10)
ax.set_facecolor("#111318")
for wl, color, name in lines:
    ax.plot([wl, wl], [1.2, 8.0], color=color, lw=4.0)
    ax.text(wl, 8.5, name, fontsize=13, color=color, ha="center")
    ax.text(wl, 0.2, f"{wl:.0f}", fontsize=9.5, color=GRAY, ha="center")
ax.text(570, 0.2, "单位：nm", fontsize=10, color=GRAY, ha="center")
ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_spectrum.png")


# ---------- fig_orbits.png  玻尔分立轨道 r ∝ n^2 ----------
fig, ax = plt.subplots(figsize=(5.6, 5.6))
fig.patch.set_facecolor(PAPER)
ax.set_xlim(-12, 12); ax.set_ylim(-12, 12)
ax.set_aspect("equal"); ax.axis("off")
nucleus = Circle((0, 0), 0.55, facecolor=OCHRE, edgecolor="none", zorder=5)
ax.add_patch(nucleus)
for n, color in [(1, TEAL), (2, TEAL), (3, GRAY)]:
    r = 1.15 * n**2
    circ = Circle((0, 0), r, fill=False, edgecolor=color, lw=2.2 if n < 3 else 1.4,
                  zorder=3)
    ax.add_patch(circ)
    ax.plot([r], [0], marker="o", ms=9 if n < 3 else 7,
            color=TEAL if n < 3 else GRAY, zorder=6)
    ax.text(r + 0.35, 0.55, f"$n={n}$", fontsize=13, color=INK, zorder=7)
ax.text(0, -11.5, r"$r_n=n^2\,\hbar^2/(e^2\mu)\propto n^2$", fontsize=13.5,
        color=INK, ha="center")
save(fig, "fig_orbits.png")


# ---------- fig_levels.png  能级图与谱线系 ----------
fig, ax = plt.subplots(figsize=(6.8, 5.0))
fig.patch.set_facecolor(PAPER)
ax.set_xlim(0, 10); ax.set_ylim(-15.5, 2.5)
En = {n: -13.6 / n**2 for n in range(1, 5)}
for n, E in En.items():
    ax.plot([1.0, 6.6], [E, E], color=TEAL, lw=2.4)
    ax.text(0.75, E, f"$n={n}$", fontsize=11.5, color=INK, va="center", ha="right")
    ax.text(6.75, E, f"{E:.2f}", fontsize=10, color=GRAY, va="center")
ax.plot([1.0, 6.6], [0, 0], color=GRAY, lw=1.1, ls="--")
ax.text(6.75, 0, "0（电离）", fontsize=10, color=GRAY, va="center")
ax.text(3.8, 0.3, "更高能级渐密，趋于 0", fontsize=9.5, color=GRAY, ha="center")
# 巴耳末系（到 n=2）
for n in [3, 4]:
    ax.annotate("", xy=(3.0, En[2] - 0.08), xytext=(3.0, En[n] + 0.08),
                arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.8,
                                mutation_scale=15))
ax.text(3.35, -5.4, "巴耳末系\n（可见光）", fontsize=11.5, color=OCHRE)
# 莱曼系（到 n=1）
for n in [2, 3]:
    ax.annotate("", xy=(1.7, En[1] - 0.08), xytext=(1.7, En[n] + 0.08),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6,
                                mutation_scale=14))
ax.text(0.95, -8.6, "莱曼系\n（紫外）", fontsize=11.5, color=INK)
ax.text(7.6, -13.2, "单位：eV", fontsize=10, color=GRAY)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_ylabel(r"能量 $E_n=-\mu e^4/(2\hbar^2 n^2)\propto -1/n^2$", fontsize=12)
save(fig, "fig_levels.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
