# -*- coding: utf-8 -*-
"""ch6-s3 中心力场 — 配图生成"""
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


# ---------- 封面图：中心与环绕壳层 ----------
fig, ax = plt.subplots(figsize=(6.2, 7.2), facecolor=TEAL)
ax.set_facecolor(TEAL)
# 中心
ax.add_patch(plt.Circle((0, 0), 0.16, color="#FFFFFF"))
# 壳层轨道
for r, a in [(0.8, 0.9), (1.5, 0.55), (2.2, 0.3)]:
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(r * np.cos(th), r * np.sin(th), color="#FFFFFF", lw=1.6, alpha=a)
# 电子点
for ang, r, c in [(0.6, 0.8, OCHRE), (2.4, 0.8, OCHRE), (1.4, 1.5, "#7FB3C8"),
                  (4.2, 1.5, "#7FB3C8"), (5.5, 2.2, "#C8D6DC")]:
    ax.plot(r * np.cos(ang), r * np.sin(ang), "o", ms=9, color=c)
# 半径箭头标注 r
ax.annotate("", xy=(0.8 * np.cos(0.6), 0.8 * np.sin(0.6)), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="#FFFFFF", lw=1.4))
ax.text(0.42, 0.32, "$r$", color="#FFFFFF", fontsize=15)
ax.text(0, -2.75, "中心力场：一切只依赖距离 $r$", ha="center",
        color="#FFFFFFCC", fontsize=13)
ax.set_xlim(-2.7, 2.7); ax.set_ylim(-3.1, 2.7)
ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 导言图：引力与库仑，同一条 -1/r 曲线 ----------
fig, ax = plt.subplots(figsize=(7.8, 4.6), facecolor=PAPER)
ax.set_facecolor(PAPER)
r = np.linspace(0.3, 6, 400)
ax.plot(r, -1 / r, color=TEAL, lw=2.4)
ax.axhline(0, color=HAIR, lw=1)
ax.annotate("万有引力  $V=-GMm/r$", xy=(2.2, -0.45), xytext=(2.6, -0.72),
            fontsize=12.5, color=INK,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))
ax.annotate("库仑吸引  $V=-e^{2}/r$", xy=(4.6, -0.217), xytext=(4.1, -0.05),
            fontsize=12.5, color=OCHRE,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))
ax.text(3.0, -1.75, "形状相同：都只是距离的函数  $V(r)$", ha="center",
        fontsize=12.5, color=GRAY)
ax.set_xlim(0, 6); ax.set_ylim(-2.0, 0.35)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel("$r$", fontsize=13)
ax.set_ylabel("$V(r)$", fontsize=13)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(HAIR)
save(fig, "fig_intro.png")


# ---------- 离心势垒：V_eff 随 l 变化 ----------
fig, ax = plt.subplots(figsize=(7.8, 4.8), facecolor=PAPER)
ax.set_facecolor(PAPER)
r = np.linspace(0.12, 6, 600)
ax.plot(r, -1 / r, color=INK, lw=2.2, label="$l=0$：只有 $V(r)$")
for l, c in [(1, TEAL), (2, OCHRE)]:
    ax.plot(r, -1 / r + l * (l + 1) / (2 * r**2), color=c, lw=2.2,
            label=f"$l={l}$：$V(r)+\\dfrac{{l(l+1)\\hbar^2}}{{2\\mu r^2}}$")
ax.axhline(0, color=HAIR, lw=1)
ax.set_xlim(0, 6); ax.set_ylim(-3.2, 4.0)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel("$r$", fontsize=13)
ax.set_ylabel("等效势（示意）", fontsize=12.5)
ax.legend(fontsize=11.5, frameon=False, loc="upper right")
ax.text(3.0, -2.6, "角动量给粒子筑起一道「离心势垒」——$l$ 越大越难靠近中心",
        ha="center", fontsize=12, color=GRAY)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(HAIR)
save(fig, "fig_centrifugal.png")


# ---------- 课外图：从行星轨道到原子壳层 ----------
fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.2), facecolor=PAPER)
ax = axes[0]
ax.set_facecolor(PAPER)
# 开普勒椭圆
t = np.linspace(0, 2 * np.pi, 300)
ax.plot(1.5 * np.cos(t) + 0.4, 1.0 * np.sin(t), color=TEAL, lw=2)
ax.plot(0, 0, "o", ms=10, color=OCHRE)
ax.plot(1.5 + 0.4, 0, "o", ms=6, color=INK)
ax.text(0.5, -1.65, "开普勒问题（1687 的经典版）", ha="center",
        fontsize=11.5, color=INK)
ax.set_xlim(-1.8, 2.4); ax.set_ylim(-1.9, 1.5)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)

ax = axes[1]
ax.set_facecolor(PAPER)
# 氢原子壳层
ax.add_patch(plt.Circle((0, 0), 0.14, color=OCHRE))
for rr in [0.7, 1.3]:
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(rr * np.cos(th), rr * np.sin(th), color=TEAL, lw=1.8, alpha=0.8)
ax.plot(0.7, 0, "o", ms=6, color=INK)
ax.text(0.1, -1.75, "氢原子（1926 的量子版）", ha="center",
        fontsize=11.5, color=INK)
ax.set_xlim(-1.8, 1.9); ax.set_ylim(-1.9, 1.5)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
fig.suptitle("同一个 $-1/r$ 势，同一套中心力场数学", fontsize=13,
             color=INK, y=1.02, fontweight="bold")
save(fig, "fig_extra.png")
