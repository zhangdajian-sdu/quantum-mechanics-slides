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

MEDIA = Path(__file__).parent / "media"
MEDIA.mkdir(exist_ok=True)

rng = np.random.default_rng(7)

# ---------------------------------------------------------------- fig_cover
# 波函数分解为本征态叠加 -> 概率柱状图（深 teal 底）
fig = plt.figure(figsize=(4.8, 5.7), dpi=200)
fig.patch.set_facecolor(PANEL_TEAL)

# top: psi decomposed into eigenfunctions
ax1 = fig.add_axes([0.10, 0.60, 0.82, 0.32])
ax1.set_facecolor(PANEL_TEAL)
ax1.grid(False)
x = np.linspace(0, 1, 400)
comps = [
    (0.62, np.exp(-((x - 0.26) / 0.13) ** 2)),
    (0.42, np.exp(-((x - 0.55) / 0.10) ** 2)),
    (0.24, np.exp(-((x - 0.82) / 0.07) ** 2)),
]
psi = sum(a * c for a, c in comps)
psi = psi / np.sqrt(np.trapezoid(psi**2, x))
ax1.plot(x, psi, color="white", lw=2.4)
ax1.fill_between(x, 0, psi, color="white", alpha=0.14)
for a, c in comps:
    ax1.plot(x, a * c, color="#F2B27E", lw=1.1, alpha=0.75, ls=(0, (4, 3)))
ax1.set_xticks([]); ax1.set_yticks([])
for s in ax1.spines.values():
    s.set_color("#FFFFFF33")
ax1.set_title(r"$\psi=\sum_n c_n\,\varphi_n$（虚线为各本征态成分）",
              color="white", fontsize=11.5, pad=8)

# bottom: probability bars
ax2 = fig.add_axes([0.10, 0.09, 0.82, 0.36])
ax2.set_facecolor(PANEL_TEAL)
ax2.grid(False)
labels = [r"$f_0$", r"$f_1$", r"$f_2$"]
probs = [0.55, 0.32, 0.13]
bars = ax2.bar(range(3), probs, width=0.52, color=["#F2B27E", "#7FB3C4", "#8A8F98"])
for i, p in enumerate(probs):
    ax2.text(i, p + 0.025, rf"$|c_{i}|^2={p:.2f}$", ha="center",
             color="white", fontsize=11)
ax2.set_xticks(range(3)); ax2.set_xticklabels(labels, color="white", fontsize=12)
ax2.set_yticks([])
for s in ["left", "right", "top"]:
    ax2.spines[s].set_visible(False)
ax2.spines["bottom"].set_color("#FFFFFF44")
ax2.set_ylim(0, 0.72)
ax2.set_title(r"测 $F$：得 $f_n$ 的概率 $P_n=|c_n|^2$", color="white",
              fontsize=11.5, pad=8)

fig.savefig(MEDIA / "fig_cover.png", facecolor=PANEL_TEAL)
plt.close(fig)

# ---------------------------------------------------------------- fig_intro
# 叠加态测量统计：psi = (phi0 + phi1)/sqrt(2)，N=1000 次测量直方图
fig = plt.figure(figsize=(8.3, 5.6), dpi=200)
fig.patch.set_facecolor(PAPER)

ax1 = fig.add_axes([0.09, 0.13, 0.40, 0.74])
ax1.set_facecolor(PAPER)
ax1.grid(False)
ax1.bar([0, 1], [0.5, 0.5], width=0.42, color=[TEAL, OCHRE])
ax1.set_xticks([0, 1])
ax1.set_xticklabels([r"$E_0=\frac{1}{2}\hbar\omega$", r"$E_1=\frac{3}{2}\hbar\omega$"],
                    fontsize=11.5)
ax1.set_yticks([])
for s in ["left", "right", "top"]:
    ax1.spines[s].set_visible(False)
ax1.spines["bottom"].set_color(GRAY)
ax1.set_ylim(0, 0.68)
for i, p in enumerate([0.5, 0.5]):
    ax1.text(i, p + 0.03, rf"$|c_{i}|^2={p}$", ha="center", fontsize=12, color=INK)
ax1.set_title(r"理论上：$\psi=(\varphi_0+\varphi_1)/\sqrt{2}$ 的概率",
              fontsize=12.5, color=INK, pad=10)

ax2 = fig.add_axes([0.57, 0.13, 0.40, 0.74])
ax2.set_facecolor(PAPER)
ax2.grid(False)
N = 1000
n1 = int(rng.binomial(N, 0.5))
counts = [N - n1, n1]
ax2.bar([0, 1], counts, width=0.42, color=[TEAL, OCHRE], alpha=0.85)
ax2.set_xticks([0, 1])
ax2.set_xticklabels([r"$E_0$", r"$E_1$"], fontsize=11.5)
ax2.set_yticks([])
for s in ["left", "right", "top"]:
    ax2.spines[s].set_visible(False)
ax2.spines["bottom"].set_color(GRAY)
ax2.set_ylim(0, 660)
for i, c in enumerate(counts):
    ax2.text(i, c + 14, f"{c} 次", ha="center", fontsize=12, color=INK)
ax2.set_title(f"实验上：重复制备同态，测 {N} 次", fontsize=12.5, color=INK, pad=10)

fig.savefig(MEDIA / "fig_intro.png", facecolor=PAPER, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- fig_avg
# 概率加权平均值示意：bars with mean line
fig = plt.figure(figsize=(7.6, 4.6), dpi=200)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0.07, 0.13, 0.88, 0.74])
ax.set_facecolor(PAPER)
ax.grid(False)
ns = np.arange(0, 6)
c2 = np.array([0.05, 0.18, 0.34, 0.25, 0.13, 0.05])
c2 = c2 / c2.sum()
ax.bar(ns, c2, width=0.55, color=TEAL, alpha=0.9)
mean = float((ns * c2).sum())
ax.axvline(mean, color=OCHRE, lw=2.4, ls=(0, (5, 3)))
ax.text(mean + 0.08, 0.36, r"$\overline{F}=\sum_n|c_n|^2f_n$", color=OCHRE,
        fontsize=13)
for n, p in zip(ns, c2):
    ax.text(n, p + 0.012, f"{p:.2f}", ha="center", fontsize=10, color=INK)
ax.set_xticks(ns)
ax.set_xticklabels([rf"$f_{n}$" for n in ns], fontsize=11)
ax.set_yticks([])
for s in ["left", "right", "top"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRAY)
ax.set_ylim(0, 0.44)
fig.savefig(MEDIA / "fig_avg.png", facecolor=PAPER, bbox_inches="tight")
plt.close(fig)

print("done:", sorted(p.name for p in MEDIA.glob("*.png")))
