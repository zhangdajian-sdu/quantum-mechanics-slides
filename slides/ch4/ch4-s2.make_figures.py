"""第四章 §4.2 插图：封面 + 引入 + 正交 + Schmidt + 完备 + 谐振子例题 + 子空间"""
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


def clean(ax, bottom=True):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRAY)
    if not bottom:
        ax.spines["bottom"].set_visible(False)


# ---------- 封面题图：正交归一 + 展开（保留） ----------
fig, ax = plt.subplots(figsize=(4.6, 6.2))
fig.patch.set_facecolor(PANEL_TEAL)
ax.set_facecolor(PANEL_TEAL)

ax.text(5.0, 9.3, r"$(\psi_m,\psi_n)=\delta_{mn}$", color="#FFFFFFB3",
        fontsize=15, ha="center")
ax.text(5.0, 8.5, r"$\psi=\sum_n c_n\psi_n$", color=OCHRE,
        fontsize=16, ha="center")

origin = (2.6, 4.6)
ax.annotate("", xy=(origin[0] + 2.6, origin[1]), xytext=origin,
            arrowprops=dict(arrowstyle="-|>", color=LIGHT, lw=2.2))
ax.annotate("", xy=(origin[0], origin[1] + 2.4), xytext=origin,
            arrowprops=dict(arrowstyle="-|>", color=LIGHT, lw=2.2))
ax.text(5.35, 4.35, r"$\psi_1$", color=LIGHT, fontsize=14, ha="center")
ax.text(2.35, 7.25, r"$\psi_2$", color=LIGHT, fontsize=14, ha="center")

psi_tip = (origin[0] + 2.1, origin[1] + 1.7)
ax.annotate("", xy=psi_tip, xytext=origin,
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.6))
ax.text(psi_tip[0] + 0.12, psi_tip[1] + 0.12, r"$\psi$", color=OCHRE, fontsize=16)

ax.plot([psi_tip[0], psi_tip[0]], [origin[1], psi_tip[1]],
        color=LIGHT, lw=1.1, ls="--", alpha=0.75)
ax.plot([origin[0], psi_tip[0]], [psi_tip[1], psi_tip[1]],
        color=LIGHT, lw=1.1, ls="--", alpha=0.75)
ax.text(4.75, 5.15, r"$c_1\psi_1$", color="#FFFFFFB3", fontsize=11.5, ha="center")
ax.text(2.28, 6.35, r"$c_2\psi_2$", color="#FFFFFFB3", fontsize=11.5,
        ha="right", rotation=90)

ns = np.arange(1, 6)
heights = [0.62, 0.25, 0.09, 0.03, 0.01]
for n, h in zip(ns, heights):
    ax.bar(n + 2.4, h * 1.9, width=0.52, bottom=0.6,
           color=OCHRE if n == 1 else LIGHT, alpha=0.95 if n == 1 else 0.7)
    ax.text(n + 2.4, 0.38, f"{n}", color="#FFFFFF99", fontsize=10, ha="center")
ax.text(5.9, 2.75, r"$|c_n|^2$", color=LIGHT, fontsize=13, ha="center")

ax.set_xlim(0, 10)
ax.set_ylim(0, 10.2)
ax.axis("off")
fig.savefig(OUT / "fig_cover.png", dpi=220, bbox_inches="tight", facecolor=PANEL_TEAL)
plt.close(fig)

# ---------- 引入页：矢量分解类比（修正：删"投影真的是实数吗"） ----------
fig, ax = plt.subplots(figsize=(7.2, 3.6))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

O = (1.0, 0.8)
ax.annotate("", xy=(O[0] + 4.6, O[1]), xytext=O,
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.4))
ax.annotate("", xy=(O[0], O[1] + 2.6), xytext=O,
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.4))
ax.text(O[0] + 4.75, O[1] - 0.28, r"$\varphi_1$", color=TEAL, fontsize=14)
ax.text(O[0] - 0.35, O[1] + 2.72, r"$\varphi_2$", color=TEAL, fontsize=14)

tip = (O[0] + 3.4, O[1] + 2.0)
ax.annotate("", xy=tip, xytext=O,
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.8))
ax.text(tip[0] + 0.15, tip[1] + 0.05, r"$\psi$", color=OCHRE, fontsize=16)

ax.plot([tip[0], tip[0]], [O[1], tip[1]], color=GRAY, lw=1.2, ls="--")
ax.plot([O[0], tip[0]], [tip[1], tip[1]], color=GRAY, lw=1.2, ls="--")
ax.text(tip[0] - 0.9, O[1] - 0.34, r"$c_1=(\varphi_1,\psi)$", color=INK, fontsize=11.5)
ax.text(O[0] - 0.18, tip[1] + 0.18, r"$c_2=(\varphi_2,\psi)$", color=INK,
        fontsize=11.5, ha="right")

ax.text(7.6, 2.5, "几何直觉：", fontsize=12, color=INK, weight="bold")
ax.text(7.6, 2.05, "正交基矢就像坐标轴，", fontsize=11.5, color=INK)
ax.text(7.6, 1.62, "任意态都能向上投影展开。", fontsize=11.5, color=INK)
ax.text(7.6, 1.02, "但波函数活在无穷维空间 ——", fontsize=11.5, color=OCHRE)
ax.text(7.6, 0.60, "基矢够用吗？", fontsize=11.5, color=OCHRE)
ax.text(7.6, 0.24, "（示意：系数 $c_n$ 一般可为复数）", fontsize=9.5, color=GRAY)

ax.set_xlim(0, 11.6)
ax.set_ylim(0.2, 4.0)
ax.axis("off")
fig.tight_layout()
fig.savefig(OUT / "fig_intro.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------- 正交性页：谐振子 psi0 与 psi1 正交（保留） ----------
fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.2))
fig.patch.set_facecolor(PAPER)

x = np.linspace(-3.2, 3.2, 600)
psi0 = np.exp(-x**2 / 2)
psi1 = np.sqrt(2) * x * np.exp(-x**2 / 2)

ax = axes[0]
ax.set_facecolor(PAPER)
ax.plot(x, psi0, color=TEAL, lw=2.2, label=r"$\psi_0$（偶）")
ax.plot(x, psi1, color=OCHRE, lw=2.2, label=r"$\psi_1$（奇）")
ax.axhline(0, color=GRAY, lw=0.8)
ax.legend(fontsize=10, frameon=False, loc="upper right")
ax.set_title("两个不同能量的本征函数", fontsize=12, color=INK, pad=6)
clean(ax)

ax = axes[1]
ax.set_facecolor(PAPER)
prod = psi0 * psi1
ax.fill_between(x, prod, where=prod >= 0, color=TEAL, alpha=0.25)
ax.fill_between(x, prod, where=prod < 0, color=OCHRE, alpha=0.25)
ax.plot(x, prod, color=INK, lw=1.8)
ax.axhline(0, color=GRAY, lw=0.8)
ax.set_title(r"乘积 $\psi_0^{*}\psi_1$：正负面积相消", fontsize=12, color=INK, pad=6)
ax.set_ylim(-1.15, 0.85)
ax.text(0, -0.95, r"$\int\psi_0^{*}\psi_1\,\mathrm{d}x=0$",
        fontsize=13, color=OCHRE, ha="center")
clean(ax)

fig.tight_layout()
fig.savefig(OUT / "fig_ortho.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------- Schmidt 正交化几何图：减去投影 ----------
fig, ax = plt.subplots(figsize=(7.6, 3.9))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

th = np.deg2rad(38)
e1 = np.array([1.0, 0.0])
v2 = np.array([np.cos(th), np.sin(th)])
proj = np.array([np.cos(th), 0.0])

ax.annotate("", xy=(3.6, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.6))
ax.text(3.6, -0.28, r"$\varphi_1=\psi_1$（单位向量）", color=TEAL, fontsize=12)

ax.annotate("", xy=v2 * 3.6, xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.2))
ax.text(v2[0] * 3.6 + 0.1, v2[1] * 3.6 + 0.08, r"$\varphi_2$", color=INK, fontsize=13)

ax.plot([0, proj[0] * 3.6], [0, 0], color=OCHRE, lw=4.5, alpha=0.45, solid_capstyle="round")
ax.text(proj[0] * 1.8, -0.30, "投影 $A\\varphi_1$", color=OCHRE, fontsize=11.5, ha="center")

ax.annotate("", xy=v2 * 3.6, xytext=proj * 3.6,
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.6))
ax.text((proj[0] + v2[0]) * 1.8 + 0.12, v2[1] * 1.8, "减去投影后的\n垂直分量 $\\propto\\psi_2$",
        color=OCHRE, fontsize=11.5)

ax.plot([proj[0] * 3.6, proj[0] * 3.6], [0, v2[1] * 3.6],
        color=GRAY, lw=1.0, ls=":")
ax.text(4.9, 2.3, "构造：", fontsize=12, color=INK, weight="bold")
ax.text(4.9, 1.92, r"$\psi_2=\dfrac{\varphi_2-A\varphi_1}{\sqrt{1-|A|^2}}$",
        fontsize=13.5, color=INK)
ax.text(4.9, 1.42, "先减投影，再归一化；", fontsize=11, color=INK)
ax.text(4.9, 1.10, "垂直分量自动与 $\\varphi_1$ 正交。", fontsize=11, color=INK)
ax.text(4.9, 0.62, "（示意取 $A$ 为实数；一般为复数）", fontsize=9.5, color=GRAY)

ax.set_xlim(-0.3, 8.2)
ax.set_ylim(-0.75, 2.9)
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout()
fig.savefig(OUT / "fig_schmidt.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------- 完备性示意图：e_x、e_y 缺 e_z ----------
fig, ax = plt.subplots(figsize=(7.6, 3.6))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

# 伪 3D：xy 平面平行四边形 + z 轴
plane = np.array([[0.6, 0.5], [4.4, 0.5], [5.6, 2.4], [1.8, 2.4]])
ax.fill(plane[:, 0], plane[:, 1], color=LIGHT, alpha=0.45, zorder=1)
O3 = np.array([1.6, 1.4])
ex = np.array([3.2, 0.0])
ey = np.array([0.9, 1.0])
ez = np.array([0.55, 2.0])

ax.annotate("", xy=O3 + ex, xytext=O3, arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.4), zorder=3)
ax.annotate("", xy=O3 + ey, xytext=O3, arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.4), zorder=3)
ax.annotate("", xy=O3 + ez, xytext=O3, arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.6), zorder=4)
ax.text(*(O3 + ex + [0.1, -0.15]), r"$\mathbf{e}_x$", color=TEAL, fontsize=13)
ax.text(*(O3 + ey + [-0.15, 0.12]), r"$\mathbf{e}_y$", color=TEAL, fontsize=13)
ax.text(*(O3 + ez + [0.1, 0.05]), r"$\mathbf{e}_z$ 方向", color=OCHRE, fontsize=13)

ax.text(3.0, 1.9, "由 $\\mathbf{e}_x,\\mathbf{e}_y$ 张成的平面：", fontsize=11.5, color=INK)
ax.text(3.0, 1.58, "已正交归一，能表示平面内任意向量", fontsize=11.5, color=INK)
ax.text(5.9, 2.75, "但 $\\mathbf{e}_z$ 方向的向量", fontsize=11.5, color=OCHRE)
ax.text(5.9, 2.43, "无处安放 —— 正交归一 ≠ 完备", fontsize=11.5, color=OCHRE)

ax.set_xlim(0, 9.4)
ax.set_ylim(0.1, 3.6)
ax.axis("off")
fig.tight_layout()
fig.savefig(OUT / "fig_complete.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------- 谐振子突变：两幅式（上势能、下波函数） ----------
fig, axes = plt.subplots(2, 1, figsize=(7.4, 3.9), sharex=True)
fig.patch.set_facecolor(PAPER)

x = np.linspace(-3.2, 3.2, 600)
ax = axes[0]
ax.set_facecolor(PAPER)
ax.plot(x, 0.5 * x**2, color=TEAL, lw=2.0)
ax.plot(x, 1.0 * x**2, color=OCHRE, lw=2.0)
ax.text(-3.05, 3.9, r"$V_1=\frac{1}{2}kx^2\ (t<0)$", color=TEAL, fontsize=11)
ax.text(-3.05, 6.9, r"$V_2=kx^2\ (t>0)$", color=OCHRE, fontsize=11)
ax.annotate("弹簧突然变硬\n" + r"$k\rightarrow 2k$", xy=(-2.1, 2.1), xytext=(-0.2, 6.2),
            fontsize=10.5, color=INK,
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2))
ax.set_ylim(0, 9.4)
clean(ax, bottom=False)
ax.set_title("势能：突变前后", fontsize=11.5, color=INK, pad=4)

ax = axes[1]
ax.set_facecolor(PAPER)
g1 = np.exp(-x**2 / 2) / np.pi**0.25
a2 = 2**0.25
g2 = np.sqrt(a2) * np.exp(-a2**2 * x**2 / 2) / np.pi**0.25
ax.plot(x, g1, color=TEAL, lw=2.2)
ax.plot(x, g2, color=OCHRE, lw=1.8, ls="--")
ax.axhline(0, color=GRAY, lw=0.8)
ax.text(1.55, 0.62, "旧基态 $\\psi_0(x,\\omega_1)$", color=TEAL, fontsize=11)
ax.text(1.35, -0.22, "新基态 $\\psi_0(x,\\omega_2)$（更窄）", color=OCHRE, fontsize=11)
ax.annotate("突变瞬间的实际态：\n仍是旧基态波函数", xy=(0.05, 0.72), xytext=(-3.05, 0.35),
            fontsize=10.5, color=TEAL,
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.2))
ax.set_ylim(-0.45, 1.05)
clean(ax)
ax.set_xlabel("$x$", fontsize=11, color=INK)
ax.set_title("波函数：突变瞬间来不及改变", fontsize=11.5, color=INK, pad=4)

fig.tight_layout()
fig.savefig(OUT / "fig_example2a.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------- 谐振子突变：分组概率柱状图 ----------
fig, ax = plt.subplots(figsize=(7.0, 3.4))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

groups = ["新基态\n$n=0$", r"其余偶数激发态" + "\n" + r"$n=2,4,6,\cdots$",
          r"奇数激发态" + "\n" + r"$n=1,3,5,\cdots$"]
vals = [0.985, 0.015, 0.0]
colors = [OCHRE, TEAL, GRAY]
bars = ax.bar(groups, vals, width=0.5, color=colors, alpha=0.92)
ax.text(0, 0.985 + 0.02, "≈98.5%", ha="center", fontsize=11.5, color=OCHRE)
ax.text(1, 0.015 + 0.02, "≈1.5%", ha="center", fontsize=11.5, color=TEAL)
ax.text(2, 0.02, "0", ha="center", fontsize=11.5, color=GRAY)
ax.set_ylabel(r"概率 $|c_n|^2$", fontsize=11.5, color=INK)
ax.set_ylim(0, 1.12)
ax.set_title("突变后测量新哈密顿量能量的概率分布", fontsize=12, color=INK, pad=6)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.spines["left"].set_color(GRAY)
ax.spines["bottom"].set_color(GRAY)
ax.tick_params(colors=INK, labelsize=10)

fig.tight_layout()
fig.savefig(OUT / "fig_example2b.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------- 共同本征态：子空间保持不变示意 ----------
fig, ax = plt.subplots(figsize=(7.4, 3.4))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

plane = np.array([[0.8, 0.4], [4.9, 0.4], [6.1, 2.5], [2.0, 2.5]])
ax.fill(plane[:, 0], plane[:, 1], color=LIGHT, alpha=0.5, zorder=1)
ax.text(3.3, 0.62, r"$\hat{A}$ 的本征子空间：$\hat{A}\varphi=a_n\varphi$", fontsize=11.5, color=INK)

O3 = np.array([1.8, 1.3])
v1 = np.array([1.5, 0.85])
v2 = np.array([0.7, 1.05])
ax.annotate("", xy=O3 + v1, xytext=O3, arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.4), zorder=3)
ax.annotate("", xy=O3 + v2, xytext=O3, arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.4), zorder=3)
ax.text(*(O3 + v1 + [0.08, -0.05]), r"$\varphi_n$", color=TEAL, fontsize=13)
ax.text(*(O3 + v2 + [0.08, 0.0]), r"$\hat{B}\varphi_n$", color=OCHRE, fontsize=13)

ax.text(5.6, 2.9, r"$\hat{A}(\hat{B}\varphi_n)=a_n(\hat{B}\varphi_n)$", fontsize=13, color=INK)
ax.text(5.6, 2.52, "作用 $\\hat{B}$ 后仍留在同一本征子空间，", fontsize=11, color=INK)
ax.text(5.6, 2.22, "只是方向可能改变。", fontsize=11, color=INK)

ax.set_xlim(0, 9.6)
ax.set_ylim(0.1, 3.6)
ax.axis("off")
fig.tight_layout()
fig.savefig(OUT / "fig_subspace.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------- 引入：氢原子线状光谱（巴尔末系，可见区） ----------
fig, ax = plt.subplots(figsize=(7.6, 2.9))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

# Balmer 系前四条可见谱线（波长 nm 与近似颜色）
lines = [
    (656.3, "#C0392B", r"H$\alpha$"),
    (486.1, "#1F77B4", r"H$\beta$"),
    (434.0, "#2C3E80", r"H$\gamma$"),
    (410.2, "#6C3483", r"H$\delta$"),
]
for wl, c, label in lines:
    x = 680 - wl  # 转置为从左到右波长递减（红在左）
    ax.plot([x, x], [0, 1.0], color=c, lw=3.2, solid_capstyle="round")
    ax.text(x, 1.12, label, ha="center", fontsize=11.5, color=INK)
    ax.text(x, -0.32, f"{wl:.1f}", ha="center", fontsize=10, color=GRAY)

# 系限
ax.annotate("系限 364.6 nm", xy=(680 - 364.6, 0.55), xytext=(680 - 358, 0.9),
            fontsize=10, color=GRAY,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0))
ax.plot([680 - 364.6, 680 - 364.6], [0, 0.45], color=GRAY, lw=1.2, ls="--")

ax.text(150, 0.5, "连续背景上\n没有信号——\n只有一条条分立的线", fontsize=11,
        color=INK, ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.45", fc="white", ec=GRAY, lw=0.9))

ax.set_xlim(-20, 340)
ax.set_ylim(-0.55, 1.5)
clean(ax, bottom=False)
ax.set_xlabel(r"波长 $\lambda$（nm，示意）　→　蓝端", fontsize=10.5, color=GRAY)
ax.set_yticks([])
fig.tight_layout()
fig.savefig(OUT / "fig_spectrum.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)


# ---------- 历史：能级跃迁与谱线的对应 ----------
fig, ax = plt.subplots(figsize=(7.6, 3.6))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

levels = {"E_3": 3.0, "E_2": 2.1, "E_1": 1.0}
xs, xe = 0.8, 3.6
for name, y in levels.items():
    ax.plot([xs, xe], [y, y], color=TEAL, lw=2.4)
    ax.text(xe + 0.12, y, f"${name}$", fontsize=13, color=TEAL, va="center")

transitions = [("E_3", "E_1", r"$h\nu_{31}$"), ("E_3", "E_2", r"$h\nu_{32}$"),
               ("E_2", "E_1", r"$h\nu_{21}$")]
xoff = {"E_3->E_1": 1.05, "E_3->E_2": 1.85, "E_2->E_1": 2.65}
for a_, b_, lab in transitions:
    key = f"{a_}->{b_}"
    x = xoff[key]
    ax.annotate("", xy=(x, levels[b_] + 0.06), xytext=(x, levels[a_] - 0.06),
                arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.0))
    ax.text(x + 0.1, (levels[a_] + levels[b_]) / 2, lab, fontsize=11, color=OCHRE)

ax.text(2.2, 0.35, "跃迁放出的光，频率由能级差决定：\n$h\\nu_{mn}=E_m-E_n$",
        fontsize=11.5, color=INK, ha="center")

# 右侧：对应谱线
ax.text(6.15, 3.35, "发射谱", fontsize=12, color=INK, ha="center")
spec = [(3.0, "#C0392B"), (2.1, "#2C3E80"), (1.0, "#1F77B4")]
for i, (y, c) in enumerate(spec):
    ax.plot([5.35, 7.0], [y, y], color=c, lw=3.0, solid_capstyle="round")
ax.annotate("", xy=(5.2, 2.05), xytext=(3.8, 2.05),
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.1, ls="--"))
ax.text(4.5, 2.6, "一一对应", fontsize=10.5, color=GRAY, ha="center")

ax.set_xlim(0, 7.6)
ax.set_ylim(0.1, 3.7)
ax.axis("off")
fig.tight_layout()
fig.savefig(OUT / "fig_levels.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

print("done:", [p.name for p in sorted(OUT.glob("*.png"))])
