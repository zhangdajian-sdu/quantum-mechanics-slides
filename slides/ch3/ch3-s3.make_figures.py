# -*- coding: utf-8 -*-
"""为量子力学 §3.3 一维谐振子课件生成示意图"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.special import hermite
from daimon_runtime import setup_plot

setup_plot()

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)

INK   = "#20242B"
TEAL  = "#1F4E5F"
OCHRE = "#C4622D"
GRAY  = "#8A8F98"
PAPER = "#FAF8F4"
HAIR  = "#E2DFD8"

def style_ax(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRAY)
    ax.tick_params(colors=GRAY, labelsize=8)
    ax.grid(False)

def psi_n(n, xi):
    """未归一化的谐振子波函数 e^{-xi^2/2} H_n(xi)"""
    Hn = hermite(n)
    return np.exp(-xi**2 / 2) * Hn(xi)

# ============================================================
# 封面：抛物线势 + 波函数层叠
# ============================================================
fig, ax = plt.subplots(figsize=(4.2, 7.5))
ax.set_xlim(-3, 3); ax.set_ylim(-3.2, 3.4); ax.axis("off")
x = np.linspace(-3, 3, 900)
ax.plot(x, 0.42 * x**2 - 2.6, color=INK, lw=2.0, alpha=0.75)
for n, c in [(0, TEAL), (1, OCHRE), (2, GRAY)]:
    E = -2.2 + n * 1.05
    p = psi_n(n, x * 1.35)
    p = p / np.abs(p).max() * 0.5
    ax.plot(x, E + p, color=c, lw=2.3)
    ax.axhline(E, color=c, lw=0.8, ls="--", alpha=0.4)
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
fig.savefig(OUT / "fig_cover.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ============================================================
# 图1：模型 —— 抛物线势与经典振幅
# ============================================================
fig, ax = plt.subplots(figsize=(5.2, 3.5))
x = np.linspace(-3.2, 3.2, 600)
V = 0.5 * x**2
ax.plot(x, V, color=INK, lw=2.0)
a = 2.2
E = 0.5 * a**2
ax.plot([-3.2, 3.2], [E, E], color=OCHRE, lw=1.6, ls="--")
ax.plot([-a, -a], [0, E], color=GRAY, lw=1.0, ls=":")
ax.plot([a, a], [0, E], color=GRAY, lw=1.0, ls=":")
ax.text(3.1, E + 0.14, "$E=\\frac{1}{2}\\mu\\omega^2 a^2$", fontsize=10, color=OCHRE, ha="right")
ax.text(-a, -0.42, "$-a$", fontsize=10, color=GRAY, ha="center")
ax.text(a, -0.42, "$a$", fontsize=10, color=GRAY, ha="center")
ax.text(2.9, 0.35, "$V(x)=\\frac{1}{2}\\mu\\omega^2 x^2$", fontsize=10.5, color=INK, ha="right")
ax.text(0, E - 0.75, "经典粒子在 $\\pm a$ 之间往返", fontsize=9.5, color=GRAY, ha="center")
ax.set_xlim(-3.2, 3.2); ax.set_ylim(-0.7, 4.2)
ax.set_xticks([]); ax.set_yticks([])
style_ax(ax)
fig.tight_layout()
fig.savefig(OUT / "fig_model.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ============================================================
# 图2：等间距能级
# ============================================================
fig, ax = plt.subplots(figsize=(5.6, 3.8))
x = np.linspace(-3.4, 3.4, 600)
V = 0.5 * x**2
ax.plot(x, V, color=INK, lw=2.0)
for n in range(5):
    E = n + 0.5
    xt = np.sqrt(2 * E)
    ax.plot([-xt, xt], [E, E], color=TEAL if n % 2 == 0 else OCHRE, lw=1.6)
    ax.text(xt + 0.12, E, f"$E_{n}$", fontsize=9.5, color=TEAL if n % 2 == 0 else OCHRE, va="center")
# 等间距标注
ax.annotate("", xy=(3.55, 1.5), xytext=(3.55, 0.5),
            arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.1))
ax.text(3.68, 1.0, "$\\hbar\\omega$", fontsize=10, color=GRAY, va="center")
ax.text(-3.1, 4.9, "$V(x)$", fontsize=10, color=INK)
ax.set_xlim(-3.4, 4.6); ax.set_ylim(-0.3, 5.2)
ax.set_xticks([]); ax.set_yticks([])
style_ax(ax)
fig.tight_layout()
fig.savefig(OUT / "fig_levels.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ============================================================
# 图3：波函数（画在各自能级高度上）
# ============================================================
fig, ax = plt.subplots(figsize=(9.2, 3.9))
x = np.linspace(-3.6, 3.6, 1200)
V = 0.5 * x**2
ax.plot(x, V, color=INK, lw=1.8)
colors = {0: TEAL, 1: OCHRE, 2: GRAY, 3: TEAL}
for n in range(4):
    E = n + 0.5
    xt = np.sqrt(2 * E)
    ax.plot([-xt, xt], [E, E], color=colors[n], lw=0.9, ls="--", alpha=0.5)
    p = psi_n(n, x)
    p = p / np.abs(p).max() * 0.42
    ax.plot(x, E + p, color=colors[n], lw=2.0)
    ax.text(3.7, E, f"$\\psi_{n}$", fontsize=10, color=colors[n], va="center")
ax.set_xlim(-3.6, 4.6); ax.set_ylim(-0.3, 4.2)
ax.set_xticks([]); ax.set_yticks([])
style_ax(ax)
fig.tight_layout()
fig.savefig(OUT / "fig_wavefunctions.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ============================================================
# 图4：量子 vs 经典几率分布
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.0))
for ax, n in [(axes[0], 1), (axes[1], 10)]:
    x = np.linspace(-6.5, 6.5, 2400)
    p = psi_n(n, x) ** 2
    # 归一化（数值）
    dx = x[1] - x[0]
    p /= p.sum() * dx
    # 经典分布：振幅 a_cl 由 E_n = 1/2 a^2（xi 单位下 a = sqrt(2n+1)）
    a_cl = np.sqrt(2 * n + 1)
    pcl = np.where(np.abs(x) < a_cl, 1.0 / (np.pi * np.sqrt(a_cl**2 - x**2)), np.nan)
    ax.plot(x, p, color=TEAL if n == 1 else OCHRE, lw=1.8)
    ax.fill_between(x, 0, p, color=TEAL if n == 1 else OCHRE, alpha=0.12)
    ax.plot(x, pcl, color=GRAY, lw=1.5, ls=(0, (4, 3)))
    ax.set_xlim(-6.5, 6.5)
    ax.set_ylim(0, max(p.max(), 0.45) * 1.18)
    ax.set_xticks([]); ax.set_yticks([])
    style_ax(ax)
    ax.set_title(f"$n={n}$ 时 $|\\psi_n(x)|^2$（实线）与经典分布（虚线）",
                 fontsize=10, color=INK)
axes[0].set_xlim(-4.5, 4.5)
fig.tight_layout()
fig.savefig(OUT / "fig_prob_classical.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ============================================================
# 图5：经典禁区
# ============================================================
fig, ax = plt.subplots(figsize=(5.6, 3.6))
x = np.linspace(-3.4, 3.4, 1200)
V = 0.5 * x**2
ax.plot(x, V, color=INK, lw=2.0)
n = 2
E = n + 0.5
a_cl = np.sqrt(2 * E)
# 禁区阴影
ax.fill_between(x, 0, V, where=(np.abs(x) > a_cl), color=OCHRE, alpha=0.12)
ax.plot([-3.4, 3.4], [E, E], color=TEAL, lw=1.5, ls="--")
ax.text(3.3, E + 0.13, "$E_n$", fontsize=10, color=TEAL, ha="right")
p = psi_n(n, x)
p = p / np.abs(p).max() * 0.9
ax.plot(x, E + 0.55 * p, color=TEAL, lw=2.0)
ax.plot([-a_cl, -a_cl], [0, E], color=GRAY, lw=1.0, ls=":")
ax.plot([a_cl, a_cl], [0, E], color=GRAY, lw=1.0, ls=":")
ax.text(-a_cl, -0.44, "$-a$", fontsize=10, color=GRAY, ha="center")
ax.text(a_cl, -0.44, "$a$", fontsize=10, color=GRAY, ha="center")
ax.text(2.95, 3.6, "经典禁区", fontsize=10, color=OCHRE, ha="center")
ax.text(2.95, 3.05, "$|x|>a$", fontsize=9, color=OCHRE, ha="center")
ax.set_xlim(-3.4, 3.4); ax.set_ylim(-0.7, 4.4)
ax.set_xticks([]); ax.set_yticks([])
style_ax(ax)
fig.tight_layout()
fig.savefig(OUT / "fig_forbidden.png", dpi=200, facecolor=PAPER)
plt.close(fig)

print("done:", sorted(p.name for p in OUT.glob("*.png")))


# ============================================================
# 图：双原子分子势与平衡点的抛物线近似（引入页）
# ============================================================
fig, ax = plt.subplots(figsize=(5.4, 3.5))
D, aa, r0 = 4.0, 1.1, 3.0
r = np.linspace(1.55, 8.0, 600)
V = D * (1 - np.exp(-aa * (r - r0)))**2 - D   # Morse 势，最小值 -D
ax.plot(r, V, color=INK, lw=2.0, label=None)
# 平衡点附近的抛物线近似
rp = np.linspace(r0 - 1.55, r0 + 1.55, 300)
Vp = -D + D * aa**2 * (rp - r0)**2
ax.plot(rp, Vp, color=OCHRE, lw=1.7, ls="--")
# 平衡位置标注
ax.plot(r0, -D, "o", ms=6, color=TEAL, zorder=5)
ax.annotate("平衡位置 $r_0$", xy=(r0 + 0.06, -D + 0.08), xytext=(4.6, -3.55),
            fontsize=10, color=TEAL,
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.0))
# 小振动区间
ax.annotate("", xy=(r0 - 0.9, -D + 0.42), xytext=(r0 + 0.9, -D + 0.42),
            arrowprops=dict(arrowstyle="<->", color=TEAL, lw=1.3))
ax.text(r0, -D + 0.66, "小振动：抛物线近似很好", fontsize=9.5, color=TEAL,
        ha="center")
# 大振幅偏离
ax.annotate("振幅大时偏离抛物线\n（非谐性）", xy=(1.74, 2.3),
            xytext=(3.35, 1.35), fontsize=9.5, color=OCHRE, ha="center",
            arrowprops=dict(arrowstyle="->", color=OCHRE, lw=1.0))
# 两个原子示意
ax.plot(6.0, 2.55, "o", ms=17, color=TEAL)
ax.plot(7.3, 2.55, "o", ms=13, color=OCHRE)
ax.annotate("", xy=(6.95, 2.55), xytext=(6.35, 2.55),
            arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.3))
ax.text(6.65, 3.02, "双原子分子在平衡距离附近振动", fontsize=9, color=GRAY,
        ha="center")
ax.text(1.62, -2.0, "$V(r)$", fontsize=11, color=INK, rotation=90)
ax.set_xlim(1.4, 8.0); ax.set_ylim(-4.6, 3.4)
ax.set_xlabel("原子间距 $r$", fontsize=10, color=INK)
ax.set_xticks([]); ax.set_yticks([])
style_ax(ax)
fig.tight_layout()
fig.savefig(OUT / "fig_morse.png", dpi=200, facecolor=PAPER)
plt.close(fig)

print("done:", sorted(p.name for p in OUT.glob("*.png")))

# ============================================================
# 图：把势能最低点连续放大——与抛物线重合（导言页）
# ============================================================
def morse(x, De=1.0, a_=0.9, xe=2.0):
    return De * (1 - np.exp(-a_ * (x - xe))) ** 2

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(7.6, 3.0))

# 全景
x = np.linspace(0.9, 8.0, 800)
ax1.plot(x, morse(x), color=INK, lw=1.8)
ax1.add_patch(plt.Rectangle((1.35, -0.02), 1.3, 0.28, fill=False,
                            ec=OCHRE, lw=1.4))
ax1.annotate("放大", xy=(2.0, 0.13), xytext=(4.6, 0.35),
             fontsize=9, color=OCHRE,
             arrowprops=dict(arrowstyle="->", color=OCHRE, lw=1.2))
ax1.set_title("分子势能曲线", fontsize=10, color=INK, pad=6)
ax1.set_xlabel("原子间距", fontsize=9, color=GRAY)
ax1.set_ylim(-0.08, 1.15); style_ax(ax1)

# 第一次放大
x2 = np.linspace(1.35, 2.65, 400)
ax2.plot(x2, morse(x2), color=INK, lw=1.8)
ax2.add_patch(plt.Rectangle((1.75, -0.002), 0.5, 0.045, fill=False,
                            ec=OCHRE, lw=1.4))
ax2.annotate("再放大", xy=(2.0, 0.02), xytext=(2.28, 0.16),
             fontsize=9, color=OCHRE,
             arrowprops=dict(arrowstyle="->", color=OCHRE, lw=1.2))
ax2.set_title("平衡点附近", fontsize=10, color=INK, pad=6)
ax2.set_xlim(1.35, 2.65); ax2.set_ylim(-0.01, 0.28); style_ax(ax2)

# 第二次放大：与抛物线重合
x3 = np.linspace(1.75, 2.25, 400)
V = morse(x3)
para = 0.5 * 1.0 * 0.9 ** 2 * (x3 - 2.0) ** 2  # De*a^2*(x-xe)^2
ax3.plot(x3, V, color=INK, lw=2.2, label="真实势能")
ax3.plot(x3, para, color=OCHRE, lw=1.6, ls="--", label="抛物线")
ax3.set_title("再放大：与抛物线重合", fontsize=10, color=INK, pad=6)
ax3.legend(fontsize=8, frameon=False, loc="upper left")
ax3.set_xlim(1.75, 2.25); ax3.set_ylim(-0.002, 0.05); style_ax(ax3)

fig.tight_layout()
fig.savefig(OUT / "fig_zoom.png", dpi=200, facecolor=PAPER)
plt.close(fig)

print("done:", sorted(p.name for p in OUT.glob("*.png")))
