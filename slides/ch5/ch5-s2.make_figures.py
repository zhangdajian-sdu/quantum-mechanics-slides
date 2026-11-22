"""第五章 §5.2 插图：封面题图 + 引入页示意图"""
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

# ---------- 封面题图：波函数 → 一列展开系数 ----------
fig, axes = plt.subplots(2, 1, figsize=(5.2, 6.2))
fig.patch.set_facecolor(PANEL_TEAL)

x = np.linspace(0, 6, 400)
psi = (np.sin(np.pi * x / 6) + 0.55 * np.sin(3 * np.pi * x / 6)
       + 0.3 * np.sin(5 * np.pi * x / 6))

ax = axes[0]
ax.set_facecolor(PANEL_TEAL)
ax.plot(x, psi, color=LIGHT, lw=2.2)
ax.axhline(0, color=LIGHT, lw=0.8, alpha=0.4)
ax.text(5.9, 1.35, r"$\psi(x)$", color=LIGHT, fontsize=15, ha="right")
ax.text(0.1, 1.35, "连续函数", color="#FFFFFFB3", fontsize=11, ha="left")
ax.set_xlim(0, 6)
ax.set_ylim(-1.6, 1.9)
ax.axis("off")

ax = axes[1]
ax.set_facecolor(PANEL_TEAL)
n = np.arange(1, 7)
c = np.array([1.0, 0.05, 0.55, 0.02, 0.3, 0.01])
ax.bar(n, c, width=0.42, color=OCHRE)
ax.text(6.4, 1.05, r"$\{C_n\}$", color=OCHRE, fontsize=15, ha="right")
ax.text(0.6, 1.05, "一列数（列矩阵）", color="#FFFFFFB3", fontsize=11, ha="left")
ax.set_xticks(n)
ax.set_xticklabels([f"$q_{i}$" for i in n], color="#FFFFFFB3", fontsize=9)
ax.set_yticks([])
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#FFFFFF66")
ax.tick_params(colors="#FFFFFFB3")
ax.set_ylim(0, 1.35)

fig.text(
    0.5, 0.505, r"$\psi(x)=\sum_{n}C_{n}U_{n}(x)$",
    color="#FFFFFFCC", fontsize=13, ha="center",
)
fig.savefig(OUT / "fig_cover.png", dpi=220, bbox_inches="tight", facecolor=PANEL_TEAL)
plt.close(fig)

# ---------- 引入页：连续自变量 vs 分立自变量 ----------
fig, axes = plt.subplots(2, 1, figsize=(7.0, 5.0))
fig.patch.set_facecolor(PAPER)

p = np.linspace(-5, 5, 600)
dens = np.exp(-p**2 / 3.0)
ax = axes[0]
ax.set_facecolor(PAPER)
ax.fill_between(p, dens, color=TEAL, alpha=0.15)
ax.plot(p, dens, color=TEAL, lw=2.0)
ax.axhline(0, color=GRAY, lw=0.8)
ax.set_ylabel(r"$|\varphi(p)|^2$", fontsize=10, color=INK)
ax.set_yticks([])
ax.set_xticks([])
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRAY)
ax.set_title("§5.1：自变量 p 连续取值 —— 几率密度", fontsize=12, color=INK, pad=5)

ax = axes[1]
ax.set_facecolor(PAPER)
n = np.arange(1, 7)
w = np.array([0.42, 0.24, 0.16, 0.09, 0.06, 0.03])
ax.bar(n, w, width=0.5, color=OCHRE, alpha=0.85)
ax.set_xticks(n)
ax.set_xticklabels([f"$q_{i}$" for i in n], fontsize=9.5, color=GRAY)
ax.set_ylabel(r"$|C_n|^2$", fontsize=10, color=INK)
ax.set_yticks([])
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRAY)
ax.set_title("本节：自变量 qn 分立取值 —— 一列几率", fontsize=12, color=INK, pad=5)

fig.tight_layout(h_pad=2.2)
fig.savefig(OUT / "fig_intro.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

print("done:", [p.name for p in OUT.glob("*.png")])

# ---------- 量子比特导言图：两个基状态 → 一列复数 ----------
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.4))
fig.patch.set_facecolor(PAPER)

ax = axes[0]
ax.set_facecolor(PAPER)
ax.hlines(0.25, 0.2, 0.8, color=TEAL, lw=3)
ax.hlines(0.75, 0.2, 0.8, color=OCHRE, lw=3)
ax.text(0.85, 0.25, r"$|0\rangle$，能量 $E_{0}$", fontsize=11.5, color=TEAL, va="center")
ax.text(0.85, 0.75, r"$|1\rangle$，能量 $E_{1}$", fontsize=11.5, color=OCHRE, va="center")
ax.annotate("", xy=(0.5, 0.72), xytext=(0.5, 0.28),
            arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.2))
ax.text(0.44, 0.5, "只有两个\n可能的基状态", fontsize=9.5, color=GRAY, ha="right", va="center")
ax.set_xlim(0, 1.6)
ax.set_ylim(0, 1)
ax.axis("off")
ax.set_title("一个两能级系统", fontsize=12, color=INK, pad=6)

ax = axes[1]
ax.set_facecolor(PAPER)
ax.text(0.02, 0.62, "任意状态 $=$", fontsize=13, color=INK, va="center")
ax.plot([0.36, 0.34, 0.34, 0.36], [0.46, 0.46, 0.78, 0.78], color=INK, lw=1.4)
ax.plot([0.50, 0.52, 0.52, 0.50], [0.46, 0.46, 0.78, 0.78], color=INK, lw=1.4)
ax.text(0.43, 0.70, r"$\alpha$", fontsize=14, color=INK, ha="center", va="center")
ax.text(0.43, 0.54, r"$\beta$", fontsize=14, color=INK, ha="center", va="center")
ax.text(0.02, 0.30, r"两个复数 $\alpha,\beta$ 就够，$|\alpha|^{2}+|\beta|^{2}=1$",
        fontsize=10.5, color=GRAY, va="center")
ax.bar([0.62, 0.80], [0.42, 0.18], width=0.10, color=[TEAL, OCHRE], alpha=0.85, bottom=0.06)
ax.text(0.62, 0.50, r"$|\alpha|^{2}$", fontsize=10, color=TEAL, ha="center")
ax.text(0.80, 0.26, r"$|\beta|^{2}$", fontsize=10, color=OCHRE, ha="center")
ax.text(0.71, -0.04, "测得 0 / 1 的几率", fontsize=9.5, color=GRAY, ha="center")
ax.set_xlim(0, 1)
ax.set_ylim(-0.1, 1)
ax.axis("off")
ax.set_title("态 = 一列复数", fontsize=12, color=INK, pad=6)

fig.tight_layout(w_pad=2.0)
fig.savefig(OUT / "fig_qubit.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

print("qubit fig done")
