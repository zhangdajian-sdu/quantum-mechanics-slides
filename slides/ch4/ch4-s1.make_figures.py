"""第四章 §4.1 插图：封面、算符流程图、次序对比、波包平移"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot

setup_plot()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

INK = "#20242B"
TEAL = "#1F4E5F"
OCHRE = "#C4622D"
GRAY = "#8A8F98"
PAPER = "#FAF8F4"
LIGHT = "#DCE6EA"
PANEL_TEAL = "#23586B"

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)

# ---------- 封面题图（沿用原版） ----------
fig, ax = plt.subplots(figsize=(4.6, 6.2))
fig.patch.set_facecolor(PANEL_TEAL)
ax.set_facecolor(PANEL_TEAL)

x = np.linspace(0, 10, 500)
psi = np.exp(-((x - 3.0) ** 2) / 1.6) * np.cos(2.2 * x)
phi = np.exp(-((x - 6.8) ** 2) / 2.4) * np.sin(1.6 * x)

ax.plot(x, 6.4 + 1.1 * psi, color=LIGHT, lw=2.2)
ax.axhline(6.4, color=LIGHT, lw=0.8, alpha=0.4)
ax.text(9.9, 7.6, r"$\psi(\mathbf{r})$", color=LIGHT, fontsize=15, ha="right")

ax.plot(x, 1.6 + 1.1 * phi, color=OCHRE, lw=2.2)
ax.axhline(1.6, color=LIGHT, lw=0.8, alpha=0.4)
ax.text(9.9, 0.5, r"$\varphi(\mathbf{r})$", color=OCHRE, fontsize=15, ha="right")

ax.annotate("", xy=(5.0, 2.9), xytext=(5.0, 5.6),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.4))
ax.text(5.25, 4.2, r"$\hat{F}$", color=OCHRE, fontsize=20, ha="left")

ax.text(5.0, 9.2, r"$[\hat{A},\hat{B}]=\hat{A}\hat{B}-\hat{B}\hat{A}$",
        color="#FFFFFFB3", fontsize=13, ha="center")
ax.text(5.0, 8.45, r"$[\,x,\hat{p}_x\,]=\mathrm{i}\hbar$",
        color=OCHRE, fontsize=15, ha="center")

ax.set_xlim(0, 10)
ax.set_ylim(-0.2, 10.2)
ax.axis("off")
fig.savefig(OUT / "fig_cover.png", dpi=220, bbox_inches="tight", facecolor=PANEL_TEAL)
plt.close(fig)


def opbox(ax, cx, cy, w, h, label, fc, ec, fs=13, tc=None):
    box = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                         boxstyle="round,pad=0.02,rounding_size=0.10",
                         fc=fc, ec=ec, lw=1.6)
    ax.add_patch(box)
    ax.text(cx, cy, label, ha="center", va="center", fontsize=fs,
            color=tc or ec)


def harrow(ax, x0, x1, y, color=GRAY, lw=2.0):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>",
                                 mutation_scale=16, color=color, lw=lw))


# ---------- 算符流程图：输入 -> [算符] -> 输出 ----------
fig, ax = plt.subplots(figsize=(7.6, 3.1))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

rows = [
    (2.05, r"$f(x)$", r"$\hat{D}=\dfrac{\mathrm{d}}{\mathrm{d}x}$", TEAL,
     r"$f'(x)$", "求导：输出仍是函数"),
    (0.65, r"$f(x)$", r"$\hat{S}f=(\,f\,)^{2}$", OCHRE,
     r"$(\,f(x)\,)^{2}$", "「平方」：输出也仍是函数"),
]
for y, fin, op, col, fout, note in rows:
    ax.text(0.55, y, fin, fontsize=14, color=INK, ha="center", va="center")
    harrow(ax, 1.05, 1.85, y)
    opbox(ax, 2.95, y, 2.0, 0.78, op, "#FFFFFF", col, fs=13)
    harrow(ax, 4.05, 4.75, y)
    ax.text(5.2, y, fout, fontsize=14, color=INK, ha="center", va="center")
    ax.text(5.2, y - 0.42, note, fontsize=9.5, color=GRAY, ha="center",
            va="center")

ax.text(3.8, 2.78, "算符 = 把函数变成（另一个）函数的规则",
        fontsize=12.5, color=OCHRE, ha="center")
ax.set_xlim(0, 7.6)
ax.set_ylim(0.1, 3.05)
ax.axis("off")
fig.savefig(OUT / "fig_flow.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------- 次序对比：先乘 x 再求导 vs 先求导再乘 x ----------
fig, ax = plt.subplots(figsize=(7.6, 3.1))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

ax.text(0.15, 2.42, "次序 ①", fontsize=11.5, color=TEAL, fontweight="bold",
        ha="left", va="center")
ax.text(1.55, 2.42, r"$f(x)=x^{2}$", fontsize=13, color=INK,
        ha="center", va="center")
harrow(ax, 2.05, 2.5, 2.42)
opbox(ax, 3.25, 2.42, 1.35, 0.72, r"先乘 $x$", "#FFFFFF", TEAL, fs=12)
harrow(ax, 4.0, 4.65, 2.42)
opbox(ax, 5.4, 2.42, 1.35, 0.72, r"再求导", "#FFFFFF", TEAL, fs=12)
harrow(ax, 6.15, 6.8, 2.42)
ax.text(7.25, 2.42, r"$3x^{2}$", fontsize=15, color=TEAL, fontweight="bold",
        ha="center", va="center")

ax.text(0.15, 1.12, "次序 ②", fontsize=11.5, color=OCHRE, fontweight="bold",
        ha="left", va="center")
ax.text(1.55, 1.12, r"$f(x)=x^{2}$", fontsize=13, color=INK,
        ha="center", va="center")
harrow(ax, 2.05, 2.5, 1.12)
opbox(ax, 3.25, 1.12, 1.35, 0.72, r"先求导", "#FFFFFF", OCHRE, fs=12)
harrow(ax, 4.0, 4.65, 1.12)
opbox(ax, 5.4, 1.12, 1.35, 0.72, r"再乘 $x$", "#FFFFFF", OCHRE, fs=12)
harrow(ax, 6.15, 6.8, 1.12)
ax.text(7.25, 1.12, r"$2x^{2}$", fontsize=15, color=OCHRE, fontweight="bold",
        ha="center", va="center")

ax.plot([0.35, 7.45], [1.77, 1.77], color="#E2DFD8", lw=1.0)
ax.text(3.9, 0.32, r"同一个 $f$、同样两步，次序不同，结果不同",
        fontsize=12, color=INK, ha="center")
ax.set_xlim(0, 7.6)
ax.set_ylim(0.0, 3.0)
ax.axis("off")
fig.savefig(OUT / "fig_order.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------- 波包平移：psi(x) -> psi(x-a) ----------
fig, ax = plt.subplots(figsize=(7.2, 3.3))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

xs = np.linspace(-6, 9, 800)
x0, a = -1.6, 3.6


def packet(x, c):
    return np.exp(-((x - c) ** 2) / 1.1) * np.cos(2.4 * (x - c))


ax.plot(xs, packet(xs, x0), color=GRAY, lw=2.0, ls="--", alpha=0.85)
ax.plot(xs, packet(xs, x0 + a), color=TEAL, lw=2.4)
ax.axhline(0, color=GRAY, lw=0.8)

ax.annotate("", xy=(x0 + a + 0.0, 1.28), xytext=(x0, 1.28),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.2))
ax.text(x0 + a / 2, 1.42, "向 $+x$ 方向移动 $a$", fontsize=12, color=OCHRE,
        ha="center")

ax.text(x0, -1.32, r"$\psi(x)$", fontsize=13, color=GRAY, ha="center")
# 提问页配图：不写出 ψ(x−a)，避免提前泄露「判断一」的答案（2026-09-27 验收补改）
ax.text(x0 + a, -1.32, "平移后的波包", fontsize=12, color=TEAL, ha="center")
ax.text(x0 + a + 0.5, 0.62, "形状不变", fontsize=10.5, color=TEAL, ha="left")

ax.set_xlim(-5.2, 8.4)
ax.set_ylim(-1.7, 1.75)
ax.axis("off")
fig.savefig(OUT / "fig_packet.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

print("done:", sorted(p.name for p in OUT.glob("*.png")))


# ---------- 正交图解：方势阱 psi1, psi2 与乘积的正负面积 ----------
fig, axes = plt.subplots(2, 1, figsize=(7.4, 4.4), sharex=True,
                         gridspec_kw=dict(hspace=0.42))
fig.patch.set_facecolor(PAPER)

xs = np.linspace(0, 1, 600)
psi1 = np.sqrt(2) * np.sin(np.pi * xs)
psi2 = np.sqrt(2) * np.sin(2 * np.pi * xs)
prod = psi1 * psi2

ax = axes[0]
ax.set_facecolor(PAPER)
for xv in (0, 1):
    ax.axvline(xv, color=INK, lw=2.0)
ax.axhline(0, color=GRAY, lw=0.8)
ax.plot(xs, psi1, color=TEAL, lw=2.2, label=r"$\psi_1(x)$")
ax.plot(xs, psi2, color=OCHRE, lw=2.2, label=r"$\psi_2(x)$")
ax.legend(loc="upper right", fontsize=11, frameon=False, ncol=2)
ax.text(0.5, 2.05, "两个波函数都遍布整个势阱，处处都不「躲开」对方",
        fontsize=11.5, color=INK, ha="center")
ax.set_ylim(-1.75, 2.35)
ax.set_yticks([])
ax.set_xticks([0, 1])
ax.tick_params(labelbottom=False, length=0)
for sp in ["top", "right", "left", "bottom"]:
    ax.spines[sp].set_visible(False)

ax = axes[1]
ax.set_facecolor(PAPER)
for xv in (0, 1):
    ax.axvline(xv, color=INK, lw=2.0)
ax.axhline(0, color=GRAY, lw=0.8)
ax.plot(xs, prod, color=INK, lw=1.8)
ax.fill_between(xs, prod, 0, where=prod >= 0, color=TEAL, alpha=0.35)
ax.fill_between(xs, prod, 0, where=prod < 0, color=OCHRE, alpha=0.35)
ax.text(0.22, 1.05, "正面积", fontsize=11.5, color=TEAL, ha="center")
ax.text(0.78, -1.35, "负面积", fontsize=11.5, color=OCHRE, ha="center")
ax.text(0.5, -2.15, r"$\int\psi_1^{*}\psi_2\,\mathrm{d}x=0$：正负相消，这才是「正交」",
        fontsize=12, color=INK, ha="center")
ax.set_ylim(-1.75, 1.6)
ax.set_yticks([])
ax.set_xticks([0, 1])
ax.set_xticklabels(["0", "L"], fontsize=11.5, color=INK)
ax.tick_params(length=0)
for sp in ["top", "right", "left", "bottom"]:
    ax.spines[sp].set_visible(False)
axes[1].set_title(r"乘积 $\psi_1(x)\,\psi_2(x)$", fontsize=11.5, color=INK, pad=4)

fig.savefig(OUT / "fig_ortho.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------- 表象示意图：态与算符各一行 ----------
fig, ax = plt.subplots(figsize=(6.8, 2.5))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

ax.text(0.55, 1.85, "量子态", fontsize=12.5, color=TEAL, fontweight="bold",
        ha="center", va="center")
opbox(ax, 2.6, 1.85, 2.2, 0.72, r"波函数 $\psi(x)$", "#FFFFFF", TEAL, fs=12.5)
ax.annotate("", xy=(4.6, 1.85), xytext=(3.85, 1.85),
            arrowprops=dict(arrowstyle="<|-|>", color=GRAY, lw=1.8))
opbox(ax, 5.55, 1.85, 1.7, 0.72, r"展开系数 $c_n$", "#FFFFFF", TEAL, fs=12.5)
ax.text(4.22, 2.14, "同一态", fontsize=9.5, color=GRAY, ha="center")

ax.text(0.55, 0.75, "力学量", fontsize=12.5, color=OCHRE, fontweight="bold",
        ha="center", va="center")
opbox(ax, 2.6, 0.75, 2.2, 0.72, r"微分算符 $-\mathrm{i}\hbar\partial_x$",
      "#FFFFFF", OCHRE, fs=12.5)
ax.annotate("", xy=(4.6, 0.75), xytext=(3.85, 0.75),
            arrowprops=dict(arrowstyle="<|-|>", color=GRAY, lw=1.8))
opbox(ax, 5.55, 0.75, 1.7, 0.72, r"矩阵 $p_{mn}$", "#FFFFFF", OCHRE, fs=12.5)
ax.text(4.22, 1.04, "同一算符", fontsize=9.5, color=GRAY, ha="center")

ax.plot([1.15, 6.55], [1.3, 1.3], color="#E2DFD8", lw=1.0)
ax.set_xlim(0, 6.8)
ax.set_ylim(0.2, 2.5)
ax.axis("off")
fig.savefig(OUT / "fig_rep.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

print("done:", sorted(p.name for p in OUT.glob("*.png")))
