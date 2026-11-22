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
PANEL_TEAL = "#23586B"

MEDIA = Path(__file__).parent / "media"
MEDIA.mkdir(exist_ok=True)


def gauss(x, sigma):
    return np.exp(-x**2 / (2 * sigma**2))


# ---------- fig_cover: Δx small <-> Δp large (deep teal bg) ----------
fig, axes = plt.subplots(2, 1, figsize=(5.0, 6.2), facecolor=PANEL_TEAL)
x = np.linspace(-6, 6, 800)
for ax, (sx, sp) in zip(axes, [(0.6, 1.9), (1.9, 0.6)]):
    ax.set_facecolor(PANEL_TEAL)
    ax.plot(x, gauss(x, sx), color="#FFFFFF", lw=2.4)
    ax.fill_between(x, gauss(x, sx), color="#FFFFFF", alpha=0.14)
    ax.plot(x, gauss(x, sp), color="#F0B27A", lw=2.0, ls="--")
    ax.grid(False)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#FFFFFF55")
ax0, ax1 = axes
ax0.annotate("", xy=(0.6, 0.42), xytext=(-0.6, 0.42),
             arrowprops=dict(arrowstyle="<->", color="#F0B27A", lw=1.4))
ax0.text(0, 0.52, r"$\Delta x$ 小", color="#F0B27A", ha="center", fontsize=11)
ax0.set_title("坐标空间：分布很窄", color="#FFFFFF", fontsize=11.5)
ax1.annotate("", xy=(1.9, 0.16), xytext=(-1.9, 0.16),
             arrowprops=dict(arrowstyle="<->", color="#F0B27A", lw=1.4))
ax1.text(0, 0.24, r"$\Delta p$ 大", color="#F0B27A", ha="center", fontsize=11)
ax1.set_title("动量空间：分布被迫变宽", color="#FFFFFF", fontsize=11.5)
fig.tight_layout(rect=[0, 0, 1, 1])
fig.savefig(MEDIA / "fig_cover.png", dpi=200, bbox_inches="tight", facecolor=PANEL_TEAL)
plt.close(fig)

# ---------- fig_intro: single-slit diffraction, narrow vs wide slit ----------
fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.6), facecolor=PAPER)
t = np.linspace(-4, 4, 800)
for ax, a, lab, col in [(axes[0], 0.9, "窄缝 $a$ 小", OCHRE), (axes[1], 2.2, "宽缝 $a$ 大", TEAL)]:
    ax.set_facecolor(PAPER)
    y = (np.sinc(a * t / np.pi))**2  # sinc^2 中央主极大
    ax.plot(t, y, color=col, lw=2.2)
    ax.fill_between(t, y, color=col, alpha=0.15)
    ax.grid(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(-4, 4); ax.set_ylim(0, 1.15)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.set_title(lab, fontsize=12, color=INK)
    ax.set_xlabel("屏上位置", fontsize=10.5, color=GRAY)
axes[0].annotate("衍射斑很宽", xy=(0, 0.55), xytext=(1.6, 0.8),
                 arrowprops=dict(arrowstyle="->", color=GRAY), fontsize=11, color=INK)
axes[1].annotate("衍射斑变窄", xy=(0, 0.55), xytext=(1.8, 0.8),
                 arrowprops=dict(arrowstyle="->", color=GRAY), fontsize=11, color=INK)
fig.suptitle("电子单缝衍射：缝越窄，条纹越散", fontsize=13, color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.92])
fig.savefig(MEDIA / "fig_intro.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------- fig_tradeoff: Δp vs Δx hyperbola ----------
fig, ax = plt.subplots(figsize=(6.4, 4.4), facecolor=PAPER)
ax.set_facecolor(PAPER)
dx = np.linspace(0.15, 4.0, 400)
dp = 1.0 / (2 * dx)  # 单位: Δp = ħ/(2Δx)
ax.plot(dx, dp, color=TEAL, lw=2.4)
ax.fill_between(dx, dp, 3.4, color=TEAL, alpha=0.10)
ax.fill_between(dx, 0, dp, color=OCHRE, alpha=0.12)
ax.text(2.6, 0.28, "禁戒区", color=OCHRE, fontsize=12)
ax.text(0.9, 2.2, "允许区\n" r"$\Delta x\,\Delta p\geqslant\hbar/2$", color=TEAL, fontsize=11.5)
ax.plot(1 / np.sqrt(2), 1 / np.sqrt(2), "o", color=OCHRE, ms=7)
ax.annotate("取等号的态\n（高斯最小波包）", xy=(1 / np.sqrt(2), 1 / np.sqrt(2)),
            xytext=(1.7, 1.35), arrowprops=dict(arrowstyle="->", color=GRAY),
            fontsize=10.5, color=INK)
ax.grid(False)
ax.set_xlim(0, 4); ax.set_ylim(0, 3.4)
ax.set_xlabel(r"$\Delta x$（任意单位）", fontsize=11.5)
ax.set_ylabel(r"$\Delta p$（任意单位）", fontsize=11.5)
ax.set_title("坐标宽度与动量宽度的此消彼长", fontsize=12.5, color=INK)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(MEDIA / "fig_tradeoff.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

print("done:", sorted(p.name for p in MEDIA.glob("*.png")))
