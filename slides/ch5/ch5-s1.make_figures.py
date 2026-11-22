"""第五章 §5.1 插图：封面题图 + 引入页示意图 + 例题2配图"""
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

# ---------- 封面题图：同一状态的两种面貌 ----------
fig, axes = plt.subplots(2, 1, figsize=(4.6, 6.2))
fig.patch.set_facecolor(PANEL_TEAL)

x = np.linspace(-10, 10, 600)
psi = np.exp(-(x**2) / 8.0) * np.cos(2.0 * x)
p = np.linspace(-10, 10, 600)
phi = np.exp(-((p - 2.0) ** 2) / 1.2) + 0.35 * np.exp(-((p + 2.0) ** 2) / 1.2)

ax = axes[0]
ax.set_facecolor(PANEL_TEAL)
ax.plot(x, psi, color=LIGHT, lw=2.2)
ax.axhline(0, color=LIGHT, lw=0.8, alpha=0.4)
ax.text(9.6, 0.75, r"$\psi(x)$", color=LIGHT, fontsize=15, ha="right")
ax.text(-9.6, 0.75, "坐标表象", color="#FFFFFFB3", fontsize=11, ha="left")
ax.set_xlim(-10, 10)
ax.set_ylim(-1.25, 1.25)
ax.axis("off")

ax = axes[1]
ax.set_facecolor(PANEL_TEAL)
ax.plot(p, phi, color=OCHRE, lw=2.2)
ax.axhline(0, color=LIGHT, lw=0.8, alpha=0.4)
ax.text(9.6, 0.95, r"$\varphi(p)$", color=OCHRE, fontsize=15, ha="right")
ax.text(-9.6, 0.95, "动量表象", color="#FFFFFFB3", fontsize=11, ha="left")
ax.set_xlim(-10, 10)
ax.set_ylim(-0.25, 1.45)
ax.axis("off")

axes[0].annotate(
    "",
    xy=(0.5, -0.06),
    xytext=(0.5, -0.24),
    xycoords=("data", "axes fraction"),
    textcoords=("data", "axes fraction"),
    arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.4),
)
fig.text(
    0.5, 0.505, r"$\varphi(p)=\frac{1}{\sqrt{2\pi\hbar}}\int\mathrm{e}^{-\mathrm{i}px/\hbar}\psi(x)\,\mathrm{d}x$",
    color="#FFFFFFCC", fontsize=11.5, ha="center",
)
fig.savefig(OUT / "fig_cover.png", dpi=220, bbox_inches="tight", facecolor=PANEL_TEAL)
plt.close(fig)

# ---------- 引入页：衍射图样 = 动量分布 ----------
fig, axes = plt.subplots(2, 1, figsize=(7.0, 5.0), sharex=False)
fig.patch.set_facecolor(PAPER)

y = np.linspace(-6, 6, 800)
pattern = (np.sinc(y / 1.1) ** 2) * (np.cos(2.4 * y) ** 2)

ax = axes[0]
ax.set_facecolor(PAPER)
ax.fill_between(y, pattern, color=TEAL, alpha=0.15)
ax.plot(y, pattern, color=TEAL, lw=2.0)
ax.axhline(0, color=GRAY, lw=0.8)
ax.set_xlabel(r"屏上位置 $y$（测量坐标）", fontsize=11, color=INK)
ax.set_ylabel("强度", fontsize=10, color=INK)
ax.set_yticks([])
ax.set_xticks([0])
ax.set_xticklabels(["0"], fontsize=9, color=GRAY)
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRAY)
ax.set_title("电子双缝衍射：屏上的强度分布", fontsize=12, color=INK, pad=5)

ax = axes[1]
ax.set_facecolor(PAPER)
ax.fill_between(y, pattern, color=OCHRE, alpha=0.15)
ax.plot(y, pattern, color=OCHRE, lw=2.0)
ax.axhline(0, color=GRAY, lw=0.8)
ax.set_xlabel(r"动量分量 $p_y$（测量动量）", fontsize=11, color=INK)
ax.set_ylabel(r"$|\varphi(p_y)|^2$", fontsize=10, color=INK)
ax.set_yticks([])
ax.set_xticks([0])
ax.set_xticklabels(["0"], fontsize=9, color=GRAY)
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRAY)
ax.set_title("同一条曲线，换一个读法：动量几率分布", fontsize=12, color=INK, pad=5)

fig.tight_layout(h_pad=2.0)
fig.savefig(OUT / "fig_intro.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------- 例题2配图：δ 势阱的动量表象波函数 ----------
fig, ax = plt.subplots(figsize=(7.0, 4.6))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

pp = np.linspace(-4, 4, 800)
beta = 1.0  # β = μγ/ħ 的单位
phi = np.sqrt(2 * beta**3 / np.pi) / (pp**2 + beta**2)
ax.fill_between(pp, phi, color=TEAL, alpha=0.14)
ax.plot(pp, phi, color=TEAL, lw=2.2, label=r"$\varphi(p)=\dfrac{A}{p^{2}+\beta^{2}}$")
ax.axhline(0, color=GRAY, lw=0.8)
ax.axvline(beta, color=OCHRE, lw=1.2, ls="--")
ax.axvline(-beta, color=OCHRE, lw=1.2, ls="--")
ax.annotate("", xy=(beta, 0.30), xytext=(-beta, 0.30),
            arrowprops=dict(arrowstyle="<->", color=OCHRE, lw=1.4))
ax.text(0, 0.345, r"宽度 $\sim\beta=\mu\gamma/\hbar$", color=OCHRE,
        fontsize=11.5, ha="center")
ax.set_xlabel(r"$p$（单位 $\beta$）", fontsize=11, color=INK)
ax.set_ylabel(r"$\varphi(p)$", fontsize=11, color=INK)
ax.set_yticks([])
ax.set_xticks([-1, 0, 1])
ax.set_xticklabels([r"$-\beta$", "0", r"$\beta$"], fontsize=10, color=GRAY)
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRAY)
ax.legend(fontsize=12, frameon=False, loc="upper right")
ax.set_title(r"δ 势阱束缚态：洛伦兹形动量分布", fontsize=12.5, color=INK, pad=6)

fig.tight_layout()
fig.savefig(OUT / "fig_delta.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

print("done:", [p.name for p in OUT.glob("*.png")])
