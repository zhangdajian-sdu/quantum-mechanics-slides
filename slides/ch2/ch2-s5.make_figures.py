# -*- coding: utf-8 -*-
"""§2.5 定态薛定谔方程 — 课件示意图"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot

setup_plot()

import numpy as np
import matplotlib.pyplot as plt

PAPER = "#FAF8F4"
INK = "#20242B"
TEAL = "#1F4E5F"
OCHRE = "#C4622D"
GRAY = "#8A8F98"
HAIR = "#E2DFD8"

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)


def style_ax(ax):
    ax.set_facecolor(PAPER)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(HAIR)
    ax.tick_params(colors=GRAY, labelsize=9)


# ---------------------------------------------------------------- fig 1
# 定态 vs 非定态：|psi|^2 是否随时间变化（一维无限深势阱 0<x<1）
x = np.linspace(0, 1, 600)
psi1 = np.sqrt(2) * np.sin(np.pi * x)
psi2 = np.sqrt(2) * np.sin(2 * np.pi * x)

fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.0), facecolor=PAPER)

# (a) 定态：两个时刻的 |psi1|^2 完全重合
ax = axes[0]
style_ax(ax)
rho_stat = psi1**2
ax.plot(x, rho_stat, color=TEAL, lw=2.2, label=r"$t=t_1$")
ax.plot(x, rho_stat, color=OCHRE, lw=1.6, ls=(0, (5, 3)), label=r"$t=t_2$")
ax.fill_between(x, rho_stat, color=TEAL, alpha=0.10)
ax.set_title(r"(a) 定态 $\psi_n(x,t)=e^{-iE_n t/\hbar}\psi_n(x)$",
             fontsize=11, color=INK, pad=8)
ax.set_xlabel("位置 $x$", fontsize=10, color=INK)
ax.set_ylabel(r"$|\psi(x,t)|^2$", fontsize=10, color=INK)
ax.set_xticks([]); ax.set_yticks([])
ax.set_ylim(0, 2.7)
ax.legend(fontsize=9, frameon=False, loc="upper right")
ax.text(0.5, 2.32, "两时刻曲线完全重合", ha="center", fontsize=9.5,
        color=OCHRE)

# (b) 非定态叠加：|psi1+psi2|^2 随时间振荡
ax = axes[1]
style_ax(ax)
# |psi|^2 = 1/2 (psi1^2 + psi2^2 + 2 psi1 psi2 cos(dE t / hbar))
rho_t0 = 0.5 * (psi1**2 + psi2**2 + 2 * psi1 * psi2 * 1.0)
rho_t1 = 0.5 * (psi1**2 + psi2**2 + 2 * psi1 * psi2 * (-1.0))
ax.plot(x, rho_t0, color=TEAL, lw=2.2, label=r"$t=t_1$")
ax.plot(x, rho_t1, color=OCHRE, lw=1.6, ls=(0, (5, 3)), label=r"$t=t_2$")
ax.set_title(r"(b) 叠加态 $\frac{1}{\sqrt{2}}(\psi_1+\psi_2)$：非定态",
             fontsize=11, color=INK, pad=8)
ax.set_xlabel("位置 $x$", fontsize=10, color=INK)
ax.set_xticks([]); ax.set_yticks([])
ax.set_ylim(0, 3.1)
ax.legend(fontsize=9, frameon=False, loc="upper right")
ax.text(0.5, 2.68, "几率分布随时间振荡", ha="center", fontsize=9.5,
        color=OCHRE)

fig.tight_layout(w_pad=2.5)
fig.savefig(OUT / "fig_stationary.png", dpi=220, facecolor=PAPER,
            bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- fig 2
# 高斯波包：动量分布与坐标分布的时间演化（教材例题 3 的物理图像）
fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.0), facecolor=PAPER)

# (a) |C(p)|^2 高斯分布，中心 p0，宽度 Delta p = Gamma
p = np.linspace(-2, 8, 600)
p0, Gamma = 3.0, 1.0
Cp2 = np.exp(-((p - p0) / Gamma) ** 2)
ax = axes[0]
style_ax(ax)
ax.plot(p, Cp2, color=TEAL, lw=2.2)
ax.fill_between(p, Cp2, color=TEAL, alpha=0.10)
ax.axvline(p0, color=GRAY, lw=0.9, ls=(0, (4, 3)))
ax.annotate("$p_0$", xy=(p0, -0.09), ha="center", fontsize=11, color=INK)
# 宽度标注
ax.annotate("", xy=(p0 - Gamma, 0.42), xytext=(p0 + Gamma, 0.42),
            arrowprops=dict(arrowstyle="<->", color=OCHRE, lw=1.2))
ax.annotate(r"宽度 $\Delta p = \Gamma$（不随时间变）",
            xy=(p0, 0.46), ha="center", fontsize=9.5, color=OCHRE)
ax.set_title(r"(a) 动量空间：$|C(p)|^2$ 为高斯分布", fontsize=11,
             color=INK, pad=8)
ax.set_xlabel("动量 $p$", fontsize=10, color=INK)
ax.set_xticks([]); ax.set_yticks([])
ax.set_ylim(-0.14, 1.15)

# (b) |psi(x,t)|^2：t=0 窄而高，t>0 平移且展宽
x2 = np.linspace(-6, 16, 900)
v0 = p0  # mu = 1
t2 = 2.0
dx0 = 1.0                       # Delta x(0) = hbar/Gamma，取 hbar=Gamma=1
dxt = dx0 * np.sqrt(1 + (Gamma**4 * t2**2))  # mu=hbar=1
g0 = np.exp(-((x2 - 0) / dx0) ** 2)
g1 = (dx0 / dxt) * np.exp(-((x2 - v0 * t2) / dxt) ** 2)
ax = axes[1]
style_ax(ax)
ax.plot(x2, g0, color=TEAL, lw=2.2, label=r"$t=0$：窄")
ax.plot(x2, g1, color=OCHRE, lw=2.0, ls=(0, (5, 3)),
        label=r"$t>0$：移至 $x=v_0 t$，展宽")
ax.fill_between(x2, g0, color=TEAL, alpha=0.10)
ax.fill_between(x2, g1, color=OCHRE, alpha=0.08)
ax.annotate("", xy=(0, -0.13), xytext=(v0 * t2, -0.13),
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.1))
ax.annotate("中心以 $v_0=p_0/\\mu$ 匀速移动", xy=(v0 * t2 / 2, -0.24),
            ha="center", fontsize=9, color=GRAY)
ax.set_title(r"(b) 坐标空间：$|\psi(x,t)|^2$ 扩散", fontsize=11,
             color=INK, pad=8)
ax.set_xlabel("位置 $x$", fontsize=10, color=INK)
ax.set_xticks([]); ax.set_yticks([])
ax.set_ylim(-0.30, 1.15)
ax.legend(fontsize=9, frameon=False, loc="upper right")

fig.tight_layout(w_pad=2.5)
fig.savefig(OUT / "fig_packet.png", dpi=220, facecolor=PAPER,
            bbox_inches="tight")
plt.close(fig)

print("done:", [p.name for p in OUT.glob("*.png")])

# ---------------------------------------------------------------- fig_cover
# 封面：定态——能级阶梯上的驻波。无限深势阱的 E_n ∝ n^2 能级，
# 每级托着一条驻波 psi_n；右上角一枚相位钟，示意唯一的时间依赖
# 是整体相位 e^{-iEt/hbar}（模方纹丝不动）。
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch

fig = plt.figure(figsize=(4.2, 5.0))
fig.patch.set_facecolor(TEAL)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(TEAL)

# 柔和的青碧底色辉光
yy, xx = np.mgrid[0:5:640j, 0:4.2:560j]
glow = np.exp(-(np.hypot(xx - 2.6, yy - 2.8) / 3.2) ** 2)
cmap_bg = LinearSegmentedColormap.from_list(
    "bg", ["#1A4353", "#1F4E5F", "#28596B", "#36707F"])
ax.imshow(glow, cmap=cmap_bg, origin="lower", extent=[0, 4.2, 0, 5],
          interpolation="bilinear", vmin=0, vmax=1)

# 势阱壁（两侧竖线，底部基线）
wx0, wx1 = 0.55, 3.65
ax.plot([wx0, wx0], [0.35, 4.55], color="#DCE9E655", lw=1.6)
ax.plot([wx1, wx1], [0.35, 4.55], color="#DCE9E655", lw=1.6)
ax.plot([wx0, wx1], [0.35, 0.35], color="#DCE9E655", lw=1.6)

# 四个能级：E_n ∝ n^2，驻波 psi_n 叠加在各自能级线上
xw = np.linspace(wx0, wx1, 500)
E = lambda n: n ** 2
scale = 3.6 / E(4.55)          # 把 n=4 的能级放在 y≈3.6 附近
for n in (1, 2, 3, 4):
    y0 = 0.55 + E(n) * scale
    # 能级细线
    ax.plot([wx0, wx1], [y0, y0], color="#DCE9E633", lw=0.9)
    # 驻波 psi_n（n 个半波），振幅小于与相邻能级的间距
    psi = np.sin(n * np.pi * (xw - wx0) / (wx1 - wx0))
    amp = 0.38 * scale * (E(n + 1) - E(n)) if n < 4 else 0.28
    col = "#DCE9E6" if n % 2 else "#BFD9DF"
    ax.plot(xw, y0 + amp * psi, color=col, lw=1.7, alpha=0.92)
    ax.fill_between(xw, y0, y0 + amp * psi, color=col, alpha=0.10)
    ax.text(wx1 + 0.12, y0, f"$E_{n}$", color="#DCE9E6B3",
            fontsize=10, va="center")

# 基态用赭色强调：最稳的驻波
n = 1
y0 = 0.55 + E(1) * scale
psi = np.sin(np.pi * (xw - wx0) / (wx1 - wx0))
ax.plot(xw, y0 + 0.38 * scale * (E(2) - E(1)) * psi, color=OCHRE,
        lw=2.0, alpha=0.95)

# 相位钟：整体相位 e^{-iEt/hbar} 随时间旋转
cx, cy, r = 1.05, 4.25, 0.40
th = np.linspace(0, 2 * np.pi, 100)
ax.plot(cx + r * np.cos(th), cy + r * np.sin(th), color="#DCE9E655",
        lw=1.2)
ang = np.deg2rad(125)
ax.add_patch(FancyArrowPatch((cx, cy),
                             (cx + r * 0.82 * np.cos(ang),
                              cy + r * 0.82 * np.sin(ang)),
                             arrowstyle="-|>", mutation_scale=11,
                             lw=1.6, color=OCHRE, zorder=6))
ax.text(cx + r + 0.14, cy, r"$e^{-iEt/\hbar}$", color="#DCE9E6B3",
        fontsize=10.5, va="center")

ax.set_xlim(0, 4.2)
ax.set_ylim(0, 5)
ax.axis("off")

fig.savefig(OUT / "fig_cover.png", dpi=170, facecolor=TEAL)
plt.close(fig)
print("saved fig_cover.png")

# ------------------------------------------------------------- fig_atom
# 引入页：(a) 经典图像——加速电子辐射能量、螺旋坠入原子核；(b) 真实原子的线状光谱
fig, axes = plt.subplots(1, 2, figsize=(8.6, 2.7), facecolor=PAPER)

ax = axes[0]
ax.set_facecolor(PAPER)
ax.axis("off")
t = np.linspace(0, 6 * np.pi, 800)
r = np.exp(-t / 14)
xs, ys = r * np.cos(t), r * np.sin(t)
ax.plot(xs, ys, color=GRAY, lw=1.4)
ax.plot([xs[-1]], [ys[-1]], "o", ms=5, color=INK)
ax.plot([0], [0], "o", ms=9, color=OCHRE)
ax.text(0.07, -0.18, "原子核", fontsize=9.5, color=OCHRE)
for ang, rr in [(0.7, 0.78), (2.7, 0.52)]:
    x0, y0 = rr * np.cos(ang), rr * np.sin(ang)
    u = np.linspace(0, 1, 60)
    ax.plot(x0 + u * 0.30 * np.cos(ang) + 0.028 * np.sin(u * 6 * np.pi) * np.cos(ang + np.pi / 2),
            y0 + u * 0.30 * np.sin(ang) + 0.028 * np.sin(u * 6 * np.pi) * np.sin(ang + np.pi / 2),
            color=TEAL, lw=1.1)
ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-1.15, 1.15)
ax.set_title("(a) 经典图像：加速电子不断辐射能量，\n沿螺旋线坠入原子核", fontsize=10.5, color=INK, pad=6)

ax = axes[1]
style_ax(ax)
for wl, c in [(656.3, "#C0392B"), (486.1, "#16A085"), (434.0, "#2980B9"), (410.2, "#8E44AD")]:
    ax.axvline(wl, color=c, lw=3)
ax.set_xlim(380, 700)
ax.set_ylim(0, 1)
ax.set_yticks([])
ax.set_xlabel("波长 $\lambda$ / nm", fontsize=10, color=INK)
ax.set_title("(b) 真实原子：分立的线状光谱\n（氢原子巴耳末系）", fontsize=10.5, color=INK, pad=6)

fig.tight_layout(w_pad=3.0)
fig.savefig(OUT / "fig_atom.png", dpi=220, facecolor=PAPER, bbox_inches="tight")
plt.close(fig)
print("saved fig_atom.png")
