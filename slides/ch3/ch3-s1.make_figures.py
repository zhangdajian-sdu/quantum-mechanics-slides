import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot

setup_plot()

import numpy as np
import matplotlib.pyplot as plt

MEDIA = Path(__file__).parent / "media"
MEDIA.mkdir(exist_ok=True)

TEAL = "#1F4E5F"
OCHRE = "#C4622D"
INK = "#20242B"
GRAY = "#8A8F98"
PAPER = "#FAF8F4"
HAIR = "#E2DFD8"


def new_fig(w, h, face=PAPER):
    fig, ax = plt.subplots(figsize=(w, h), dpi=100)
    fig.patch.set_facecolor(face)
    ax.set_facecolor(face)
    return fig, ax


def save(fig, name):
    fig.savefig(MEDIA / name, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print("saved", name)


def well(x):
    """光滑对称势阱（高斯型）"""
    return 3.2 * (1 - np.exp(-(x / 2.2) ** 2))


x = np.linspace(-6, 6, 1200)

# ---------- fig_cover.png : 封面，纯净势阱 ----------
fig, ax = new_fig(3.4, 5.4)
ax.plot(x, well(x), color=TEAL, lw=2.6)
ax.axhline(0, color=GRAY, lw=0.8, ls="--", alpha=0.6)
ax.set_xlim(-6, 6)
ax.set_ylim(-0.6, 4.2)
ax.axis("off")
save(fig, "fig_cover.png")

# ---------- fig_bound.png : 势阱 + 带衰减尾巴的束缚态波函数 ----------
fig, ax = new_fig(5.6, 4.0)
V = well(x)
psi = 1.35 * np.exp(-(x / 2.0) ** 2) + 1.15
ax.plot(x, V, color=INK, lw=2.0)
ax.axhline(1.15, color=GRAY, lw=0.9, ls="--", alpha=0.8)
ax.plot(x, psi, color=TEAL, lw=2.4)
ax.fill_between(x, 1.15, psi, where=(psi > 1.15), color=TEAL, alpha=0.15)
# 标注
ax.annotate("主要分布区域", xy=(0, 2.1), ha="center", fontsize=13, color=TEAL)
ax.annotate("衰减尾部", xy=(4.35, 1.65), fontsize=12, color=OCHRE)
ax.annotate("", xy=(3.6, 1.28), xytext=(4.2, 1.55),
            arrowprops=dict(arrowstyle="->", color=OCHRE, lw=1.2))
ax.annotate("衰减尾部", xy=(-5.6, 1.65), fontsize=12, color=OCHRE)
ax.annotate("", xy=(-3.6, 1.28), xytext=(-4.6, 1.55),
            arrowprops=dict(arrowstyle="->", color=OCHRE, lw=1.2))
ax.annotate("$V(x)$", xy=(4.6, 3.05), fontsize=13, color=INK)
ax.annotate("$\\psi(x)$", xy=(1.6, 2.55), fontsize=14, color=TEAL)
ax.set_xlim(-6, 6)
ax.set_ylim(0.4, 4.2)
ax.axis("off")
save(fig, "fig_bound.png")

# ---------- fig_free.png : 自由粒子的两个反向动量 ----------
fig, ax = new_fig(6.4, 3.0)
ax.axhline(0, color=HAIR, lw=1.0)
ax.annotate("", xy=(2.6, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=3.2))
ax.annotate("", xy=(-2.6, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=3.2))
ax.annotate("$+\\hbar k$", xy=(1.65, 0.28), fontsize=16, color=TEAL)
ax.annotate("$-\\hbar k$", xy=(-2.75, 0.28), fontsize=16, color=OCHRE)
ax.annotate("$\\mathrm{e}^{ikx}$", xy=(2.15, -0.62), fontsize=13, color=TEAL)
ax.annotate("$\\mathrm{e}^{-ikx}$", xy=(-3.35, -0.62), fontsize=13, color=OCHRE)
ax.annotate("同一个能量  $E=\\dfrac{\\hbar^{2}k^{2}}{2\\mu}\\ (k>0)$",
            xy=(0, -1.15), ha="center", fontsize=14, color=INK)
ax.set_xlim(-4.2, 4.2)
ax.set_ylim(-1.5, 1.0)
ax.axis("off")
save(fig, "fig_free.png")

# ---------- 宇称三幅：偶 / 奇 / 非奇非偶 ----------
def parity_panel(psi, mirror_note, fname, note_color):
    fig, ax = new_fig(4.4, 3.2)
    xx = np.linspace(-3.2, 3.2, 800)
    ax.axhline(0, color=GRAY, lw=0.9, alpha=0.7)
    ax.axvline(0, color=GRAY, lw=0.9, alpha=0.7)
    ax.plot(xx, psi(xx), color=TEAL, lw=2.4, label="$\\psi(x)$")
    ax.fill_between(xx, 0, psi(xx), where=(psi(xx) >= 0), color=TEAL, alpha=0.18)
    ax.fill_between(xx, 0, psi(xx), where=(psi(xx) < 0), color=OCHRE, alpha=0.22)
    ax.plot(xx, psi(-xx), color=GRAY, lw=1.6, ls="--", label="$\\psi(-x)$")
    ax.legend(loc="upper right", fontsize=10, frameon=False)
    ax.annotate(mirror_note, xy=(0, -2.35), ha="center", fontsize=13,
                color=note_color, weight="bold")
    ax.set_xlim(-3.4, 3.4)
    ax.set_ylim(-2.7, 2.4)
    ax.axis("off")
    save(fig, fname)


parity_panel(lambda t: 1.8 * np.exp(-(t / 1.6) ** 2),
             "翻转后不变", "fig_even.png", TEAL)
parity_panel(lambda t: 2.2 * (t / 1.6) * np.exp(-(t / 1.6) ** 2),
             "翻转后整体变号", "fig_odd.png", OCHRE)
parity_panel(lambda t: 1.7 * np.exp(-((t - 0.9) / 1.3) ** 2) + 0.5 * np.exp(-((t + 1.6) / 0.8) ** 2),
             "翻转后形状改变", "fig_neither.png", GRAY)

# ---------- fig_sympot.png : 左右对称势 ----------
fig, ax = new_fig(5.2, 3.4)
ax.plot(x, well(x), color=INK, lw=2.2)
ax.annotate("$V(-x)=V(x)$", xy=(0, 3.55), ha="center", fontsize=14, color=INK)
ax.annotate("", xy=(1.9, 2.6), xytext=(-1.9, 2.6),
            arrowprops=dict(arrowstyle="<->", color=OCHRE, lw=1.6))
ax.set_xlim(-6, 6)
ax.set_ylim(-0.4, 4.2)
ax.axis("off")
save(fig, "fig_sympot.png")

# ---------- 半边求解三图 ----------
xs = np.linspace(0, 6, 600)
Vhalf = well(xs)
psi_even_half = 1.9 * np.exp(-(xs / 2.0) ** 2)
psi_odd_half = 3.0 * (xs / 1.9) * np.exp(-(xs / 1.9) ** 2)

# 只解右半边
fig, ax = new_fig(4.4, 3.2)
ax.plot(xs, Vhalf, color=INK, lw=2.0)
ax.plot(xs, psi_even_half, color=TEAL, lw=2.4)
ax.axvline(0, color=GRAY, lw=1.0, ls="--", alpha=0.8)
ax.annotate("先只求解 $x>0$ 的半边", xy=(2.7, 3.5), fontsize=12.5, color=INK)
ax.annotate("$\\psi(x)$", xy=(1.35, 1.75), fontsize=13, color=TEAL)
ax.set_xlim(-0.3, 6)
ax.set_ylim(-0.4, 4.2)
ax.axis("off")
save(fig, "fig_half_right.png")

# 补成偶态
fig, ax = new_fig(4.4, 3.2)
xe = np.linspace(-6, 6, 1200)
ax.plot(xe, well(xe), color=INK, lw=2.0)
pe = 1.9 * np.exp(-(xe / 2.0) ** 2)
ax.plot(xe, pe, color=TEAL, lw=2.4)
ax.fill_between(xe, 0, pe, color=TEAL, alpha=0.15)
ax.axvline(0, color=GRAY, lw=1.0, ls="--", alpha=0.8)
ax.annotate("偶态：$\\psi^{\\prime}(0)=0$", xy=(0, 3.5), ha="center",
            fontsize=13, color=TEAL, weight="bold")
ax.annotate("原点处斜率为零", xy=(0, 2.15), ha="center", fontsize=10.5, color=GRAY)
ax.set_xlim(-6, 6)
ax.set_ylim(-0.4, 4.2)
ax.axis("off")
save(fig, "fig_half_even.png")

# 补成奇态
fig, ax = new_fig(4.4, 3.2)
ax.plot(xe, well(xe), color=INK, lw=2.0)
po = 3.0 * (xe / 1.9) * np.exp(-(xe / 1.9) ** 2)
ax.plot(xe, po, color=TEAL, lw=2.4)
ax.fill_between(xe, 0, po, where=(po >= 0), color=TEAL, alpha=0.15)
ax.fill_between(xe, 0, po, where=(po < 0), color=OCHRE, alpha=0.2)
ax.axvline(0, color=GRAY, lw=1.0, ls="--", alpha=0.8)
ax.axhline(0, color=GRAY, lw=0.8, alpha=0.5)
ax.scatter([0], [0], s=46, color=OCHRE, zorder=5)
ax.annotate("奇态：$\\psi(0)=0$", xy=(0, 3.5), ha="center",
            fontsize=13, color=OCHRE, weight="bold")
ax.annotate("原点必为节点", xy=(0.5, -0.85), ha="left", fontsize=10.5, color=GRAY)
ax.set_xlim(-6, 6)
ax.set_ylim(-1.6, 4.2)
ax.axis("off")
save(fig, "fig_half_odd.png")

print("all figures done")
