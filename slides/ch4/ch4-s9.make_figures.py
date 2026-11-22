# -*- coding: utf-8 -*-
"""为量子力学 §4.9 维里定理与 F–H 定理课件生成示意图"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from daimon_runtime import setup_plot

setup_plot()

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)

INK   = "#20242B"
TEAL  = "#1F4E5F"
OCHRE = "#C4622D"
GRAY  = "#8A8F98"
PAPER = "#FAF8F4"

# ============================================================
# 封面：三种齐次势中 T、V 对 E 的「分成」
# ============================================================
fig, ax = plt.subplots(figsize=(3.2, 3.82))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

rows = [
    ("谐振子\n$\\nu=2$", 0.5),
    ("线性势\n$\\nu=1$", 1/3),
    ("四次势\n$\\nu=4$", 2/3),
]
ys = [2.7, 1.65, 0.6]
for (label, frac), y in zip(rows, ys):
    ax.barh(y, frac, height=0.52, color=TEAL, edgecolor="none")
    ax.barh(y, 1 - frac, left=frac, height=0.52, color=OCHRE, edgecolor="none")
    ax.text(frac / 2, y, "$\\langle T\\rangle$", ha="center", va="center",
            fontsize=9.5, color="white")
    ax.text(frac + (1 - frac) / 2, y, "$\\langle V\\rangle$", ha="center",
            va="center", fontsize=9.5, color="white")
    ax.text(-0.06, y, label, ha="right", va="center", fontsize=9.5, color=INK)

ax.text(0.5, 3.5, "各部分占 $E$ 的比例", ha="center", fontsize=10, color=GRAY)
ax.set_xlim(-0.72, 1.05)
ax.set_ylim(0.15, 3.85)
ax.axis("off")

fig.savefig(OUT / "fig_cover.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ============================================================
# 引入页：E_n 如何分成 T 与 V？
# ============================================================
fig = plt.figure(figsize=(5.2, 3.7))
fig.patch.set_facecolor(PAPER)

ax = fig.add_axes([0.05, 0.30, 0.90, 0.66])
ax.set_facecolor(PAPER)
x = np.linspace(-3.0, 3.0, 500)
ax.plot(x, 0.5 * x**2, color=INK, lw=1.5)
E = 2.5
xr = np.sqrt(2 * E)
ax.plot([-xr, xr], [E, E], color=TEAL, lw=1.8)
ax.text(xr + 0.12, E, "$E_n$", fontsize=11, color=TEAL, va="center")
ax.set_xlim(-3.2, 4.0)
ax.set_ylim(-0.05, 4.6)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.grid(False)
ax.text(-3.05, 4.25, "定态 $\\psi_n$：能量 $E_n$ 已知", fontsize=10.5, color=INK)

ax2 = fig.add_axes([0.05, 0.04, 0.90, 0.18])
ax2.set_facecolor(PAPER)
ax2.barh(0, 1.0, height=0.52, color="#D8E2E6", edgecolor=GRAY, lw=0.8)
ax2.text(0.5, 0.46, "$E_n=\\langle T\\rangle+\\langle V\\rangle$",
         ha="center", va="center", fontsize=10.5, color=INK)
ax2.text(0.27, -0.04, "$\\langle T\\rangle=\\ ?$", ha="center",
         va="center", fontsize=10.5, color=TEAL, fontweight="bold")
ax2.text(0.75, -0.04, "$\\langle V\\rangle=\\ ?$", ha="center",
         va="center", fontsize=10.5, color=OCHRE, fontweight="bold")
ax2.set_xlim(0, 1); ax2.set_ylim(-0.42, 0.62)
ax2.axis("off")

fig.savefig(OUT / "fig_intro.png", dpi=200, facecolor=PAPER,
            bbox_inches="tight")
plt.close(fig)

print("saved fig_cover.png, fig_intro.png")
