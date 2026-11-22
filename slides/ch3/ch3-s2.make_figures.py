# -*- coding: utf-8 -*-
"""为量子力学 §3.2 一维方势阱课件生成示意图"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq
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

# ============================================================
# 封面：三种方势阱层叠图案
# ============================================================
fig, ax = plt.subplots(figsize=(4.2, 7.5))
ax.set_xlim(-3, 3); ax.set_ylim(-3.2, 3.2); ax.axis("off")

x = np.linspace(-3, 3, 1200)

# 上：无限深方势阱 + 基态
y0 = 1.9
ax.fill_between(x, y0 - 1.15, y0 + 1.15, where=(np.abs(x) > 1.3), color=TEAL, alpha=0.16)
ax.plot(x, y0 + 0.55 * np.cos(np.pi * x / 2.6) * (np.abs(x) <= 1.3), color=TEAL, lw=2.4)
ax.axhline(y0, color=TEAL, lw=0.8, ls="--", alpha=0.4)

# 中：有限深方势阱 + 泄漏波函数
y0 = 0.0
ax.fill_between(x, y0 - 1.0, y0 + 1.0, where=(np.abs(x) > 1.3), color=OCHRE, alpha=0.14)
psi = np.cos(np.pi * x / 3.4) * (np.abs(x) <= 1.3)
tails = np.sign(np.cos(np.pi * 1.3 / 3.4)) * np.exp(-(np.abs(x) - 1.3) * 1.6) * abs(np.cos(np.pi * 1.3 / 3.4))
psi = np.where(np.abs(x) <= 1.3, psi, tails)
ax.plot(x, y0 + 0.55 * psi, color=OCHRE, lw=2.4)
ax.axhline(y0, color=OCHRE, lw=0.8, ls="--", alpha=0.4)

# 下：半壁无限高势阱 + 波函数
y0 = -1.9
ax.fill_between(x, y0 - 1.0, y0 + 1.0, where=(x < -1.3), color=GRAY, alpha=0.22)
ax.fill_between(x, y0 - 1.0, y0 + 0.55, where=(x > 1.3), color=GRAY, alpha=0.10)
xs = np.linspace(-1.3, 3, 400)
psih = np.sin(np.pi * (xs + 1.3) / 3.2) * np.exp(-np.maximum(xs - 1.3, 0) * 1.1)
ax.plot(xs, y0 + 0.6 * psih, color=INK, lw=2.2, alpha=0.8)
ax.axhline(y0, color=GRAY, lw=0.8, ls="--", alpha=0.4)

fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
fig.savefig(OUT / "fig_cover.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ============================================================
# 图1：无限深方势阱 —— 势场、能级与波函数
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.4))

ax = axes[0]
a = 2.0
ax.fill_between([-3, 0], 0, 9, color=TEAL, alpha=0.14)
ax.fill_between([a, 5], 0, 9, color=TEAL, alpha=0.14)
ax.plot([-3, 0], [0, 0], color=INK, lw=1.6)
ax.plot([a, 5], [0, 0], color=INK, lw=1.6)
ax.plot([0, 0], [0, 9], color=INK, lw=1.6)
ax.plot([a, a], [0, 9], color=INK, lw=1.6)
for n in range(1, 5):
    E = 0.5 * n**2
    ax.plot([0, a], [E, E], color=OCHRE, lw=1.4)
    ax.text(2.15, E, f"$E_{n}$", fontsize=9, color=OCHRE, va="center")
ax.text(-0.12, 8.55, "$V\\to\\infty$", fontsize=8, color=GRAY, ha="right")
ax.text(2.6, 8.0, "$V(x)$", fontsize=10, color=INK)
ax.text(0, -0.62, "0", fontsize=9, color=GRAY, ha="center")
ax.text(a, -0.62, "a", fontsize=9, color=GRAY, ha="center")
ax.set_xlim(-1.2, 4.6); ax.set_ylim(-0.9, 9.0)
ax.set_xticks([]); ax.set_yticks([])
style_ax(ax)
ax.set_title("势场与能级  $E_n=n^2\\pi^2\\hbar^2/2\\mu a^2$", fontsize=10, color=INK)

ax = axes[1]
xs = np.linspace(0, a, 500)
for n, c in [(1, TEAL), (2, OCHRE), (3, GRAY)]:
    E = 0.5 * n**2
    psi = np.sqrt(2 / a) * np.sin(n * np.pi * xs / a)
    ax.plot(xs, E + 0.62 * psi, color=c, lw=2.0)
    ax.plot([0, a], [E, E], color=c, lw=0.8, ls="--", alpha=0.45)
    ax.text(2.12, E, f"$\\psi_{n}$", fontsize=9, color=c, va="center")
ax.plot([0, 0], [0, 9], color=INK, lw=1.6)
ax.plot([a, a], [0, 9], color=INK, lw=1.6)
ax.text(0, -0.62, "0", fontsize=9, color=GRAY, ha="center")
ax.text(a, -0.62, "a", fontsize=9, color=GRAY, ha="center")
ax.set_xlim(-0.5, 4.2); ax.set_ylim(-0.9, 9.0)
ax.set_xticks([]); ax.set_yticks([])
style_ax(ax)
ax.set_title("定态波函数  $\\psi_n=\\sqrt{2/a}\\,\\sin(n\\pi x/a)$", fontsize=10, color=INK)

fig.tight_layout()
fig.savefig(OUT / "fig_inf_well.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ============================================================
# 图2：无限深方势阱几率密度
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(9.2, 2.9))
for ax, n, c in [(axes[0], 1, TEAL), (axes[1], 2, OCHRE)]:
    xs = np.linspace(0, a, 500)
    p = (2 / a) * np.sin(n * np.pi * xs / a) ** 2
    ax.plot(xs, p, color=c, lw=2.2)
    ax.fill_between(xs, 0, p, color=c, alpha=0.15)
    ax.plot([0, 0], [0, 1.15], color=INK, lw=1.4)
    ax.plot([a, a], [0, 1.15], color=INK, lw=1.4)
    ax.set_xlim(-0.3, 2.3); ax.set_ylim(0, 1.25)
    ax.set_xticks([0, a]); ax.set_xticklabels(["0", "a"], fontsize=9)
    ax.set_yticks([])
    style_ax(ax)
    ax.set_title(f"$|\\psi_{n}(x)|^2$（{'基态' if n == 1 else '第一激发态'}）", fontsize=10, color=c)
fig.tight_layout()
fig.savefig(OUT / "fig_inf_prob.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ============================================================
# 图3：有限深方势阱分区
# ============================================================
fig, ax = plt.subplots(figsize=(5.4, 3.4))
V0 = 3.0; ah = 1.3
ax.fill_between([-4, -ah], 0, V0, color=TEAL, alpha=0.13)
ax.fill_between([ah, 4], 0, V0, color=TEAL, alpha=0.13)
ax.plot([-4, -ah], [V0, V0], color=INK, lw=1.6)
ax.plot([ah, 4], [V0, V0], color=INK, lw=1.6)
ax.plot([-ah, -ah], [0, V0], color=INK, lw=1.6)
ax.plot([ah, ah], [0, V0], color=INK, lw=1.6)
ax.plot([-4, 4], [0, 0], color=INK, lw=1.2)
E = 1.1
ax.plot([-4, 4], [E, E], color=OCHRE, lw=1.6, ls="--")
ax.text(3.9, E + 0.12, "$E$", fontsize=11, color=OCHRE, ha="right")
ax.text(-3.9, V0 + 0.12, "$V_0$", fontsize=11, color=INK)
ax.text(-2.6, 1.9, "Ⅰ", fontsize=13, color=TEAL, ha="center", fontweight="bold")
ax.text(0, 1.9, "Ⅱ", fontsize=13, color=TEAL, ha="center", fontweight="bold")
ax.text(2.6, 1.9, "Ⅲ", fontsize=13, color=TEAL, ha="center", fontweight="bold")
ax.text(-ah, -0.34, "$-a/2$", fontsize=9, color=GRAY, ha="center")
ax.text(ah, -0.34, "$a/2$", fontsize=9, color=GRAY, ha="center")
ax.text(-2.6, 0.55, "$A\\,e^{\\alpha x}$", fontsize=9.5, color=GRAY, ha="center")
ax.text(0, 0.55, "$\\cos kx$ / $\\sin kx$", fontsize=9.5, color=GRAY, ha="center")
ax.text(2.6, 0.55, "$F\\,e^{-\\alpha x}$", fontsize=9.5, color=GRAY, ha="center")
ax.set_xlim(-4, 4); ax.set_ylim(-0.5, 3.6)
ax.set_xticks([]); ax.set_yticks([])
style_ax(ax)
fig.tight_layout()
fig.savefig(OUT / "fig_finite_regions.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ============================================================
# 图4：图解法求能级（ζ–η 平面）
# ============================================================
G = 4.0
fig, ax = plt.subplots(figsize=(4.9, 4.2))
zet = np.linspace(0.02, G - 0.02, 600)

# 圆
ax.plot(zet, np.sqrt(G**2 - zet**2), color=INK, lw=1.8)
ax.text(3.35, 2.35, "$\\zeta^2+\\eta^2=G^2$", fontsize=10, color=INK, rotation=-38,
        bbox=dict(facecolor=PAPER, edgecolor="none", alpha=0.85, pad=1.5))

# 偶宇称曲线 η = ζ tan ζ（分段）
for lo, hi in [(0.02, np.pi / 2 - 0.06), (np.pi / 2 + 0.06, np.pi - 0.04), (np.pi + 0.04, 3 * np.pi / 2 - 0.08)]:
    z = np.linspace(lo, hi, 300)
    ax.plot(z, z * np.tan(z), color=TEAL, lw=1.8)

# 奇宇称曲线 η = -ζ cot ζ（分段，虚线）
for lo, hi in [(0.06, np.pi - 0.06), (np.pi + 0.06, 2 * np.pi - 0.1)]:
    z = np.linspace(lo, hi, 300)
    ax.plot(z, -z / np.tan(z), color=OCHRE, lw=1.8, ls=(0, (5, 3)))

# 渐近线
for zv in [np.pi / 2, np.pi, 3 * np.pi / 2]:
    ax.axvline(zv, color=HAIR, lw=0.9, zorder=0)

# 数值交点
f_even = lambda z: z * np.tan(z) - np.sqrt(G**2 - z**2)
f_odd = lambda z: -z / np.tan(z) - np.sqrt(G**2 - z**2)
roots = []
for (f, lo, hi) in [(f_even, 0.05, np.pi / 2 - 0.05), (f_odd, np.pi / 2 + 0.05, np.pi - 0.05),
                    (f_even, np.pi + 0.05, 3 * np.pi / 2 - 0.05)]:
    hi = min(hi, G - 0.02)  # 求根区间不能越过圆的定义域 ζ < G，否则 sqrt 出 NaN，符号判断失效漏根
    if f(lo) * f(hi) < 0:
        r = brentq(f, lo, hi)
        roots.append(r)
        ax.plot(r, np.sqrt(G**2 - r**2), "o", ms=7, color=INK, mfc="white", mew=1.6, zorder=5)

ax.text(1.05, 2.1, "$\\eta=\\zeta\\tan\\zeta$（偶宇称）", fontsize=9.5, color=TEAL,
        bbox=dict(facecolor=PAPER, edgecolor="none", alpha=0.85, pad=1.5))
ax.text(2.35, 0.75, "$\\eta=-\\zeta\\cot\\zeta$（奇宇称）", fontsize=9.5, color=OCHRE,
        bbox=dict(facecolor=PAPER, edgecolor="none", alpha=0.85, pad=1.5))
ax.set_xlabel("$\\zeta=ka/2$", fontsize=10, color=INK)
ax.set_ylabel("$\\eta=\\alpha a/2$", fontsize=10, color=INK)
ax.set_xticks([np.pi / 2, np.pi, 3 * np.pi / 2])
ax.set_xticklabels(["$\\pi/2$", "$\\pi$", "$3\\pi/2$"], fontsize=9)
ax.set_xlim(0, 5.2); ax.set_ylim(0, 5.2)
style_ax(ax)
fig.tight_layout()
fig.savefig(OUT / "fig_graphical.png", dpi=200, facecolor=PAPER)
plt.close(fig)
print("graphical roots:", roots)

# ============================================================
# 图5：有限深方势阱波函数（含隧穿尾部）
# ============================================================
def even_state(zeta, G, ah=1.3):
    k = zeta / ah
    alpha = np.sqrt(G**2 - zeta**2) / ah
    x = np.linspace(-4, 4, 1600)
    D = 1.0
    A = D * np.cos(k * ah) * np.exp(alpha * ah)
    psi = np.where(np.abs(x) <= ah, D * np.cos(k * x),
                   A * np.exp(-alpha * np.abs(x)))
    return x, psi

def odd_state(zeta, G, ah=1.3):
    k = zeta / ah
    alpha = np.sqrt(G**2 - zeta**2) / ah
    x = np.linspace(-4, 4, 1600)
    D = 1.0
    A = D * np.sin(k * ah) * np.exp(alpha * ah)
    psi = np.where(np.abs(x) <= ah, D * np.sin(k * x),
                   np.sign(x) * A * np.exp(-alpha * np.abs(x)))
    return x, psi

z1, z2 = roots[0], roots[1]
fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.1))
for ax, (zeta, fn, c, lab) in zip(axes, [
        (z1, even_state, TEAL, "偶宇称基态"),
        (z2, odd_state, OCHRE, "奇宇称第一激发态")]):
    x, psi = fn(zeta, G)
    psi = psi / np.abs(psi).max() * 0.85
    ax.fill_between([-4, -ah], 0, 2.6, color=c, alpha=0.08)
    ax.fill_between([ah, 4], 0, 2.6, color=c, alpha=0.08)
    ax.plot([-ah, -ah], [0, 2.6], color=GRAY, lw=1.2)
    ax.plot([ah, ah], [0, 2.6], color=GRAY, lw=1.2)
    ax.plot(x, 1.0 + psi, color=c, lw=2.2)
    ax.axhline(1.0, color=c, lw=0.8, ls="--", alpha=0.45)
    ax.text(0, 0.25, lab, fontsize=10, color=c, ha="center")
    ax.text(-ah, -0.28, "$-a/2$", fontsize=8.5, color=GRAY, ha="center")
    ax.text(ah, -0.28, "$a/2$", fontsize=8.5, color=GRAY, ha="center")
    ax.annotate("指数衰减尾部", xy=(2.1, 1.0 + psi[np.argmin(np.abs(x - 2.1))]),
                xytext=(2.6, 2.1), fontsize=9, color=GRAY,
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.9))
    ax.set_xlim(-4, 4); ax.set_ylim(-0.45, 2.7)
    ax.set_xticks([]); ax.set_yticks([])
    style_ax(ax)
fig.tight_layout()
fig.savefig(OUT / "fig_finite_psi.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ============================================================
# 图6：半壁无限高方势阱
# ============================================================
fig, ax = plt.subplots(figsize=(5.6, 3.3))
V0 = 2.6; aH = 2.0
ax.fill_between([-1.5, 0], 0, 4.4, color=GRAY, alpha=0.24)
ax.fill_between([aH, 5], 0, V0, color=TEAL, alpha=0.13)
ax.plot([0, 0], [0, 4.4], color=INK, lw=1.6)
ax.plot([aH, aH], [0, V0], color=INK, lw=1.6)
ax.plot([aH, 5], [V0, V0], color=INK, lw=1.6)
ax.plot([-1.5, 5], [0, 0], color=INK, lw=1.2)
ax.text(4.9, V0 + 0.12, "$V_0$", fontsize=11, color=INK, ha="right")
ax.text(-0.55, 4.15, "$V\\to\\infty$", fontsize=9, color=GRAY)

# 波函数：井内 sin，井外指数衰减（示意）
xs = np.linspace(0, 5, 800)
kH = np.pi / (aH * 1.28)
psi = np.sin(kH * xs) * (xs <= aH)
tail = np.sin(kH * aH) * np.exp(-(xs - aH) * 1.5) * (xs > aH)
psi = np.where(xs <= aH, np.sin(kH * xs), np.sin(kH * aH) * np.exp(-(xs - aH) * 1.5))
ax.plot(xs, 0.9 + 0.85 * psi, color=OCHRE, lw=2.2)
ax.axhline(0.9, color=OCHRE, lw=0.8, ls="--", alpha=0.45)
ax.text(4.9, 1.0, "$E$", fontsize=11, color=OCHRE, ha="right")
ax.text(0, -0.34, "0", fontsize=9, color=GRAY, ha="center")
ax.text(aH, -0.34, "a", fontsize=9, color=GRAY, ha="center")
ax.text(1.0, 2.35, "$A\\sin kx$", fontsize=10, color=GRAY, ha="center")
ax.text(3.6, 1.75, "$B\\,e^{-\\alpha x}$", fontsize=10, color=GRAY, ha="center")
ax.set_xlim(-1.5, 5); ax.set_ylim(-0.5, 4.6)
ax.set_xticks([]); ax.set_yticks([])
style_ax(ax)
fig.tight_layout()
fig.savefig(OUT / "fig_half_well.png", dpi=200, facecolor=PAPER)
plt.close(fig)

print("done:", sorted(p.name for p in OUT.glob("*.png")))


# ============================================================
# 图：量子限域——势阱变窄，能级间隔变大（引入页）
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.0, 3.5))

def draw_well(ax, x0, w, levels, title):
    H = 17.5
    # 无限深壁
    ax.plot([x0, x0], [0, H], color=INK, lw=2.0)
    ax.plot([x0 + w, x0 + w], [0, H], color=INK, lw=2.0)
    ax.plot([x0, x0 + w], [0, 0], color=INK, lw=2.0)
    for i, (E, lab) in enumerate(levels):
        c = TEAL if i == 0 else OCHRE
        ax.plot([x0 + 0.12, x0 + w - 0.12], [E, E], color=c, lw=1.8)
        ax.text(x0 + w + 0.16, E - 0.5, lab, fontsize=11, color=c)
    ax.set_title(title, fontsize=11, color=INK, pad=8)
    ax.set_xlim(x0 - 1.1, x0 + w + 1.6); ax.set_ylim(-0.8, H)
    ax.set_xticks([]); ax.set_yticks([])
    ax.axis("off")

draw_well(ax1, 0, 4.0, [(1.0, "$E_1$"), (4.0, "$E_2$")], "阱宽 $a$")
draw_well(ax2, 1.0, 2.0, [(4.0, "$E_1'$"), (16.0, "$E_2'$")], "阱宽 $a/2$")
# 能级间隔标注
ax1.annotate("", xy=(-0.55, 4.0), xytext=(-0.55, 1.0),
             arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.2))
ax1.text(-0.75, 2.5, "$\\Delta E$", fontsize=10, color=GRAY, ha="right",
         va="center")
ax2.annotate("", xy=(0.45, 16.0), xytext=(0.45, 4.0),
             arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.2))
ax2.text(0.25, 10.0, "$\\Delta E'=4\\,\\Delta E$", fontsize=10, color=GRAY,
         ha="right", va="center")
fig.tight_layout()
fig.savefig(OUT / "fig_confinement.png", dpi=200, facecolor=PAPER)
plt.close(fig)

print("done:", sorted(p.name for p in OUT.glob("*.png")))

# ============================================================
# 图：预测投票——宽 a 与宽 a/2 的两个无限深阱（不标数值关系）
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.0, 3.4))

def draw_well2(ax, x0, w, levels, title):
    H = 15.0
    ax.plot([x0, x0], [0, H], color=INK, lw=2.0)
    ax.plot([x0 + w, x0 + w], [0, H], color=INK, lw=2.0)
    ax.plot([x0, x0 + w], [0, 0], color=INK, lw=2.0)
    for i, (E, lab) in enumerate(levels):
        c = TEAL if i == 0 else OCHRE
        ax.plot([x0 + 0.12, x0 + w - 0.12], [E, E], color=c, lw=1.8)
        ax.text(x0 + w + 0.18, E - 0.5, lab, fontsize=11, color=c)
    ax.set_title(title, fontsize=11, color=INK, pad=8)
    ax.set_xlim(x0 - 1.2, x0 + w + 1.7); ax.set_ylim(-0.8, H)
    ax.set_xticks([]); ax.set_yticks([])
    ax.axis("off")

# 窄阱能级画得更高更疏，但故意不按精确比例，避免提前泄露答案
draw_well2(ax1, 0, 4.0, [(1.0, "$E_1$"), (4.2, "$E_2$")], "阱宽 $a$")
draw_well2(ax2, 1.0, 2.0, [(3.4, "$E_1'$"), (12.6, "$E_2'$")], "阱宽 $a/2$")
ax1.annotate("", xy=(-0.55, 4.2), xytext=(-0.55, 1.0),
             arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.2))
ax1.text(-0.72, 2.6, "$\Delta E$", fontsize=10, color=GRAY, ha="right",
         va="center")
ax2.annotate("", xy=(0.45, 12.6), xytext=(0.45, 3.4),
             arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.2))
ax2.text(0.22, 8.0, "$\Delta E'=?$", fontsize=10, color=GRAY, ha="right",
         va="center")
fig.tight_layout()
fig.savefig(OUT / "fig_predict.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ============================================================
# 图：无限深方势阱 —— 仅势场（供 08 页模型页使用，无结果剧透）
# ============================================================
fig, ax = plt.subplots(figsize=(6.4, 2.6))
a = 2.0
ax.fill_between([-3, 0], 0, 9, color=TEAL, alpha=0.16)
ax.fill_between([a, 5], 0, 9, color=TEAL, alpha=0.16)
ax.plot([-3, 0], [0, 0], color=INK, lw=1.8)
ax.plot([a, 5], [0, 0], color=INK, lw=1.8)
ax.plot([0, 0], [0, 9], color=INK, lw=1.8)
ax.plot([a, a], [0, 9], color=INK, lw=1.8)
ax.text(-1.6, 4.4, "$V\\to\\infty$", fontsize=10, color=GRAY, ha="center")
ax.text(3.6, 4.4, "$V\\to\\infty$", fontsize=10, color=GRAY, ha="center")
ax.text(1.0, 1.3, "$V=0$", fontsize=11, color=TEAL, ha="center")
ax.annotate("", xy=(a - 0.06, 0.35), xytext=(0.06, 0.35),
            arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0))
ax.text(1.0, 0.55, "阱宽 $a$", fontsize=9.5, color=GRAY, ha="center")
ax.text(0, -0.7, "0", fontsize=9.5, color=GRAY, ha="center")
ax.text(a, -0.7, "a", fontsize=9.5, color=GRAY, ha="center")
ax.text(4.9, -0.7, "$x$", fontsize=10, color=GRAY)
ax.text(-1.15, 8.2, "$V(x)$", fontsize=10.5, color=INK)
ax.set_xlim(-2.6, 5.2); ax.set_ylim(-1.1, 9.0)
ax.set_xticks([]); ax.set_yticks([])
style_ax(ax)
fig.tight_layout()
fig.savefig(OUT / "fig_well_only.png", dpi=200, facecolor=PAPER)
plt.close(fig)

print("done:", sorted(p.name for p in OUT.glob("*.png")))
