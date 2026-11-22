# -*- coding: utf-8 -*-
"""ch6-s4 氢原子 — 配图生成"""
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
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print("saved", name)


# ---------- 封面图：氢原子能级与跃迁（深青底） ----------
fig, ax = plt.subplots(figsize=(6.2, 7.4), facecolor=TEAL)
ax.set_facecolor(TEAL)
for n in range(1, 6):
    E = -13.6 / n**2
    ax.hlines(E, 0.15, 0.85, color="#FFFFFF", lw=2.2, alpha=0.95)
    ax.text(0.87, E, f"$n={n}$", color="#FFFFFFCC", fontsize=12, va="center")
ax.hlines(0, 0.15, 0.85, color="#FFFFFF", lw=1.2, alpha=0.4)
ax.text(0.87, 0, "$E=0$", color="#FFFFFF80", fontsize=11, va="center")
# 跃迁箭头：2->1（莱曼α），3->2（巴尔末α 红），4->2
for n1, n2, c, x in [(2, 1, "#FFD27F", 0.35), (3, 2, "#FF8C69", 0.55),
                     (4, 2, "#9FD3E8", 0.72)]:
    ax.annotate("", xy=(x, -13.6 / n2**2), xytext=(x, -13.6 / n1**2),
                arrowprops=dict(arrowstyle="->", color=c, lw=2))
ax.text(0.30, -8.2, "莱曼 $\\alpha$", color="#FFD27F", fontsize=10.5, ha="center")
ax.text(0.50, -4.6, "H$\\alpha$ 656 nm", color="#FF8C69", fontsize=10.5,
        ha="center")
ax.set_xlim(0, 1.15); ax.set_ylim(-14.6, 1.2)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
fig.text(0.5, 0.04, "氢原子能级 $E_n=-13.6\\,\\mathrm{eV}/n^2$ 与谱线跃迁",
         ha="center", color="#FFFFFFCC", fontsize=12)
save(fig, "fig_cover.png")


# ---------- 导言图：-1/r 势阱与其中的分立能级 ----------
fig, ax = plt.subplots(figsize=(7.8, 4.8), facecolor=PAPER)
ax.set_facecolor(PAPER)
r = np.linspace(0.35, 8, 500)
ax.plot(r, -1 / r * 3.4, color=TEAL, lw=2.4)
ax.axhline(0, color=HAIR, lw=1)
for n in range(1, 4):
    E = -3.4 / n**2
    ax.hlines(E, 0.5, 7.5, color=OCHRE, lw=1.8, alpha=0.9)
    ax.text(7.6, E, f"$E_{n}$", fontsize=11.5, color=OCHRE, va="center")
ax.text(4.0, -3.9, "库仑势 $V=-e^{2}/r$ 与它的分立束缚能级",
        ha="center", fontsize=12.5, color=INK)
ax.set_xlim(0, 8.6); ax.set_ylim(-4.2, 0.5)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel("$r$", fontsize=13)
ax.set_ylabel("能量（示意）", fontsize=12.5)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(HAIR)
save(fig, "fig_intro.png")


# ---------- 能级图：E_n 与 n² 简并 ----------
fig, ax = plt.subplots(figsize=(7.8, 4.8), facecolor=PAPER)
ax.set_facecolor(PAPER)
for n in range(1, 5):
    E = -13.6 / n**2
    ax.hlines(E, 0.1, 0.55, color=INK, lw=2)
    ax.text(0.585, E, f"$n={n}$，${E:.2f}$ eV", fontsize=11.5,
            va="center", color=INK)
    deg = n**2
    if deg <= 9:
        for k in range(deg):
            ax.plot(1.12 + 0.028 * k, E, "o", ms=5, color=OCHRE)
        ax.text(1.12 + 0.028 * deg + 0.03, E, f"{deg} 重简并",
                fontsize=11, va="center", color=OCHRE)
    else:
        ax.text(1.12, E, f"… {deg} 重简并",
                fontsize=11, va="center", color=OCHRE)
ax.hlines(0, 0.1, 0.55, color=GRAY, lw=1)
ax.text(0.585, 0.15, "电离限 $E=0$", fontsize=10.5, color=GRAY, va="center")
ax.text(1.12, 1.2, "$n^{2}=\\sum_{l=0}^{n-1}(2l+1)$", fontsize=11.5,
        va="center", color=GRAY)
ax.set_xlim(0, 1.75); ax.set_ylim(-14.8, 2.2)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_levels.png")


# ---------- 径向几率分布 W_nl = R² r²（Z=1, a=1） ----------
def R(n, l, r):
    if (n, l) == (1, 0):
        return 2 * np.exp(-r)
    if (n, l) == (2, 0):
        return 2 * (1 / 2)**1.5 * (1 - r / 2) * np.exp(-r / 2)
    if (n, l) == (2, 1):
        return (1 / np.sqrt(3)) * (1 / 2)**1.5 * r * np.exp(-r / 2)

fig, ax = plt.subplots(figsize=(7.8, 4.8), facecolor=PAPER)
ax.set_facecolor(PAPER)
r = np.linspace(0.001, 20, 1000)
for (n, l), c, lb in [((1, 0), INK, "1s"), ((2, 0), TEAL, "2s"),
                      ((2, 1), OCHRE, "2p")]:
    W = R(n, l, r)**2 * r**2
    ax.plot(r, W / W.max(), color=c, lw=2.2, label=lb)
ax.plot(1, 1.02, "v", color=INK, ms=7)
ax.text(1, 1.09, "最可几半径 $r=a$", ha="center", fontsize=11, color=INK)
ax.set_xlim(0, 20); ax.set_ylim(0, 1.2)
ax.set_xticks([0, 5, 10, 15, 20])
ax.set_yticks([])
ax.set_xlabel("$r\\,/\\,a$（玻尔半径）", fontsize=12.5)
ax.set_ylabel("$W_{nl}(r)=R_{nl}^{2}\\,r^{2}$（各自归一到峰值）", fontsize=12)
ax.legend(fontsize=12, frameon=False)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(HAIR)
save(fig, "fig_radial.png")


# ---------- 课外图：玻尔轨道 vs 薛定谔几率云 ----------
fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.2), facecolor=PAPER)
ax = axes[0]
ax.set_facecolor(PAPER)
ax.plot(0, 0, "o", ms=9, color=OCHRE)
for rr in [0.5, 1.0, 1.5]:
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(rr * np.cos(th), rr * np.sin(th), color=TEAL, lw=1.6, alpha=0.85)
ax.plot(1.0, 0, "o", ms=6, color=INK)
ax.text(0, -1.95, "玻尔 1913：电子走圆周轨道", ha="center", fontsize=11.5,
        color=INK)
ax.set_xlim(-1.9, 1.9); ax.set_ylim(-2.2, 1.8)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)

ax = axes[1]
ax.set_facecolor(PAPER)
rng = np.random.default_rng(7)
# 1s 几率云散点
r = rng.gamma(2.0, 0.5, 2200)
th = rng.uniform(0, 2 * np.pi, 2200)
ax.scatter(r * np.cos(th), r * np.sin(th), s=2, color=TEAL, alpha=0.35)
ax.plot(0, 0, "o", ms=9, color=OCHRE)
ax.text(0, -1.95, "薛定谔 1926：几率云 $|\\psi|^{2}$", ha="center",
        fontsize=11.5, color=INK)
ax.set_xlim(-1.9, 1.9); ax.set_ylim(-2.2, 1.8)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_extra.png")
