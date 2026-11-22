# -*- coding: utf-8 -*-
"""为量子力学 §3.4 势垒穿透课件生成示意图"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from daimon_runtime import setup_plot

setup_plot()

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)

INK   = "#20242B"
TEAL  = "#1F4E5F"
OCHRE = "#C4622D"
GRAY  = "#8A8F98"
PAPER = "#FFFFFF"
HAIR  = "#E2DFD8"

def style_ax(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRAY)
    ax.tick_params(colors=GRAY, labelsize=10.5)
    ax.grid(False)

# ============================================================
# 封面：波穿过势垒的抽象图案
# ============================================================
fig, ax = plt.subplots(figsize=(4.2, 7.5))
ax.set_xlim(-3, 3); ax.set_ylim(-3.2, 3.2); ax.axis("off")
x = np.linspace(-3, 3, 1600)
for y0, E_frac, c in [(1.9, 0.45, TEAL), (0.0, 0.30, OCHRE), (-1.9, 0.6, GRAY)]:
    # 势垒
    ax.fill_between([-0.7, 0.7], y0 - 1.0, y0 + 1.0, color=c, alpha=0.13)
    ax.plot([-0.7, -0.7], [y0 - 1.0, y0 + 1.0], color=c, lw=1.2, alpha=0.5)
    ax.plot([0.7, 0.7], [y0 - 1.0, y0 + 1.0], color=c, lw=1.2, alpha=0.5)
    # 左侧驻波
    xl = x[x <= -0.7]
    wavel = (1.0 * np.cos(4.5 * xl) + 0.45 * np.cos(4.5 * xl + 1.2)) * 0.42
    # 垒内衰减
    xb = x[(x > -0.7) & (x <= 0.7)]
    waveb = np.exp(-(xb + 0.7) * 1.8) * np.cos(2.0 * xb) * 0.42 * 1.1
    # 右侧透射小波
    xr = x[x > 0.7]
    waver = 0.42 * E_frac * np.cos(4.5 * xr + 0.6)
    ax.plot(xl, y0 + wavel, color=c, lw=2.1)
    ax.plot(xb, y0 + waveb, color=c, lw=2.1)
    ax.plot(xr, y0 + waver, color=c, lw=2.1)
    ax.axhline(y0, color=c, lw=0.7, ls="--", alpha=0.35)
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
fig.savefig(OUT / "fig_cover.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ============================================================
# 图1：矩形势垒模型（三区）—— 无文字版，标签在 PPT 中添加
# ============================================================
fig, ax = plt.subplots(figsize=(5.6, 3.4))
V0 = 2.6; a = 2.0
ax.fill_between([0, a], 0, V0, color=TEAL, alpha=0.15)
ax.plot([-2.5, 0], [0, 0], color=INK, lw=1.6)
ax.plot([a, 4.5], [0, 0], color=INK, lw=1.6)
ax.plot([0, 0], [0, V0], color=INK, lw=1.6)
ax.plot([a, a], [0, V0], color=INK, lw=1.6)
ax.plot([0, a], [V0, V0], color=INK, lw=1.6)
E = 1.1
ax.plot([-2.5, 4.5], [E, E], color=OCHRE, lw=1.5, ls="--")
# 入射/反射/透射箭头（不含文字）
ax.annotate("", xy=(-0.25, 0.42), xytext=(-1.6, 0.42),
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.4))
ax.annotate("", xy=(-1.6, 0.16), xytext=(-0.5, 0.16),
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))
ax.annotate("", xy=(4.2, 0.42), xytext=(2.6, 0.42),
            arrowprops=dict(arrowstyle="->", color=OCHRE, lw=1.4))
ax.set_xlim(-2.5, 4.5); ax.set_ylim(-0.55, 3.2)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
# 固定边距，保证数据坐标到图幅的映射确定，便于在 PPT 中叠加标签
fig.subplots_adjust(left=0.03, right=0.98, top=0.96, bottom=0.10)
fig.savefig(OUT / "fig_model.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ============================================================
# 图2：T 与 R 随 E/V0 的变化（含共振透射）
# ============================================================
def T_of_E(E, V0=1.0, a=2.0):
    E = np.asarray(E, dtype=float)
    T = np.empty_like(E)
    k2 = E
    hi = E > V0
    lo = ~hi
    al2 = E[hi] - V0
    T[hi] = (4 * k2[hi] * al2) / ((k2[hi] - al2)**2 * np.sin(np.sqrt(al2) * a)**2 + 4 * k2[hi] * al2)
    be2 = V0 - E[lo]
    sh = np.sinh(np.sqrt(np.maximum(be2, 1e-12)) * a)
    den = (k2[lo] + be2)**2 * sh**2 + 4 * k2[lo] * be2
    T[lo] = np.where(den > 0, (4 * k2[lo] * be2) / np.maximum(den, 1e-30), 0.0)
    return T

fig, ax = plt.subplots(figsize=(6.4, 3.5))
# 加宽势垒（a=20），把前几个共振拉到垒顶附近展开：
# 非共振处反射明显，共振峰严格达到 T=1
a_wide = 20.0
E = np.linspace(1.001, 1.27, 4000)
T = T_of_E(E, a=a_wide)
ax.plot(E, T, color=TEAL, lw=2.0)
ax.axhline(1.0, color=GRAY, lw=1.0, ls="--")
ax.text(1.263, 1.025, "$T=1$", fontsize=10.5, color=GRAY, ha="right")
# 共振点：E_n = V0 + n^2 π^2 / a^2（单位 ħ²/2μ=1, V0=1）
for n, lab in [(1, "\\pi"), (2, "2\\pi"), (3, "3\\pi")]:
    Er = 1.0 + n**2 * np.pi**2 / a_wide**2
    ax.plot(Er, 1.0, "o", ms=7, color=OCHRE, mfc="white", mew=1.7, zorder=5)
    ax.annotate("$\\alpha a=" + lab + "$",
                xy=(Er, 1.0), xytext=(Er - 0.018, 1.16 if n == 2 else 1.13),
                fontsize=10.5, color=OCHRE, ha="center",
                arrowprops=dict(arrowstyle="->", color=OCHRE, lw=0.9))
ax.set_xlabel("$E\\,/\\,V_0$（无量纲单位 $\\hbar^2/2\\mu=1$，取 $V_0=1,\\ a=20$）", fontsize=11, color=INK)
ax.set_ylabel("透射率 $T$", fontsize=11.5, color=INK)
ax.set_xlim(1.0, 1.27); ax.set_ylim(0, 1.28)
style_ax(ax)
fig.tight_layout()
fig.savefig(OUT / "fig_resonance.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ============================================================
# 图3：E<V0 时穿过势垒的波函数（实部）—— 真实求解
# ============================================================
V0, aB, E0 = 1.0, 2.0, 0.45
k = np.sqrt(E0); be = np.sqrt(V0 - E0)
# 4x4 线性方程组求解 B,F,G,C（A=1）
M = np.array([
    [1, -1, -1, 0],
    [-1j * k, -be, be, 0],
    [0, np.exp(be * aB), np.exp(-be * aB), -np.exp(1j * k * aB)],
    [0, be * np.exp(be * aB), -be * np.exp(-be * aB), -1j * k * np.exp(1j * k * aB)],
], dtype=complex)
rhs = np.array([-1, -1j * k, 0, 0], dtype=complex)
B, F, G, C = np.linalg.solve(M, rhs)
Tval = abs(C)**2

x1 = np.linspace(-6, 0, 700)
x2 = np.linspace(0, aB, 300)
x3 = np.linspace(aB, 8, 700)
psi1 = np.exp(1j * k * x1) + B * np.exp(-1j * k * x1)
psi2 = F * np.exp(be * x2) + G * np.exp(-be * x2)
psi3 = C * np.exp(1j * k * x3)

fig, ax = plt.subplots(figsize=(8.6, 3.2))
y0 = 0.0
ax.fill_between([0, aB], -1.8, 1.8, color=TEAL, alpha=0.12)
ax.plot([0, 0], [-1.8, 1.8], color=GRAY, lw=1.1)
ax.plot([aB, aB], [-1.8, 1.8], color=GRAY, lw=1.1)
ax.plot(x1, y0 + psi1.real, color=TEAL, lw=1.9)
ax.plot(x2, y0 + psi2.real, color=TEAL, lw=1.9)
ax.plot(x3, y0 + psi3.real, color=TEAL, lw=1.9)
ax.axhline(y0, color=GRAY, lw=0.7, ls="--", alpha=0.4)
ax.text(-4.9, 1.35, "入射波 + 反射波（干涉）", fontsize=9.5, color=GRAY)
ax.text(0.28, 1.35, "垒内指数衰减", fontsize=9.5, color=GRAY)
ax.text(4.6, 1.35, f"透射波（$T={Tval:.3f}$）", fontsize=9.5, color=OCHRE)
ax.text(0, -2.1, "0", fontsize=9, color=GRAY, ha="center")
ax.text(aB, -2.1, "a", fontsize=9, color=GRAY, ha="center")
ax.set_ylabel(r"纵轴：$\mathrm{Re}\,\psi$（实部）", fontsize=9.5, color=INK)
ax.set_xlim(-6, 8); ax.set_ylim(-2.35, 1.95)
ax.set_xticks([]); ax.set_yticks([])
style_ax(ax)
fig.tight_layout()
fig.savefig(OUT / "fig_tunneling_wave.png", dpi=200, facecolor=PAPER)
plt.close(fig)
print("T(E=0.45V0) =", Tval)

# ============================================================
# 图4：T 对垒宽 a 的敏感性（电子例子，对数坐标）
# ============================================================
mu_e, hbar = 1.0, 1.0  # 相对单位
# 用书上的电子例子：V0=10 eV, E=2 eV
# beta a ∝ a；T ≈ 16E(V0-E)/V0^2 * e^{-2βa}
Ee, V0e = 2.0, 10.0
# 恢复 SI 比例：β = sqrt(2μ(V0-E))/ħ = 1.449e8 cm^-1，βa = 2.9 @ a = 0.2 nm
beta_per_nm = 2.9 / 0.2  # 每 nm
a_vals = np.linspace(0.05, 0.65, 300)  # 单位 nm
prefac = 16 * Ee * (V0e - Ee) / V0e**2
T_a = prefac * np.exp(-2 * beta_per_nm * a_vals)

fig, ax = plt.subplots(figsize=(5.8, 3.4))
ax.semilogy(a_vals, T_a, color=TEAL, lw=2.2)
for a0, t0 in [(0.2, 7.77e-3), (0.4, 2.36e-5), (0.6, 7.19e-8)]:
    ax.plot(a0, t0, "o", ms=7, color=OCHRE, mfc="white", mew=1.7, zorder=5)
# 手动标注
ax.text(0.215, 2.2e-2, "$7.77\\times10^{-3}$", fontsize=11.5, color=OCHRE)
ax.text(0.415, 6.5e-5, "$2.36\\times10^{-5}$", fontsize=11.5, color=OCHRE)
ax.text(0.50, 3.0e-8, "$7.19\\times10^{-8}$", fontsize=11.5, color=OCHRE)
ax.set_xlabel("垒宽 $a$（nm）", fontsize=12, color=INK)
ax.set_ylabel("透射率 $T$（对数）", fontsize=12, color=INK)
ax.set_xlim(0.05, 0.65); ax.set_ylim(1e-9, 3e-1)
style_ax(ax)
fig.tight_layout()
fig.savefig(OUT / "fig_sensitivity.png", dpi=200, facecolor=PAPER)
plt.close(fig)

print("done:", sorted(p.name for p in OUT.glob("*.png")))


# ============================================================
# 图5：α 衰变的核势示意（引入页）
# ============================================================
fig, ax = plt.subplots(figsize=(5.4, 3.4))
R = 2.0           # 核半径（示意）
Vc = 8.0          # 库仑势垒高度（示意）
r = np.linspace(R, 10, 400)
Vcoul = Vc * R / r
# 核内深势阱
ax.plot([0, R], [-3.5, -3.5], color=INK, lw=1.8)
ax.plot([R, R], [-3.5, Vc], color=INK, lw=1.8)
# 核外库仑势垒
ax.plot(r, Vcoul, color=INK, lw=1.8)
# 经典禁区（势垒区）阴影
Ea = 2.0
r2 = Vc * R / Ea
ax.fill_between([R, r2], -4.2, Ea, color=TEAL, alpha=0.10)
# α 粒子能量（只画到核边界——经典上它出不来）
ax.plot([0, R], [Ea, Ea], color=OCHRE, lw=1.5, ls="--")
ax.text(0.15, Ea + 0.25, r"$E$（α 粒子能量）", fontsize=9.5, color=OCHRE)
# 疑问：它怎么出来的？
ax.text((R + r2) / 2, Ea - 1.1, "？", fontsize=16, color=OCHRE, ha="center",
        fontweight="bold")
# 标注
ax.text(1.0, -2.6, "核内", fontsize=10, color=GRAY, ha="center")
ax.text(6.9, 5.6, "库仑势垒", fontsize=10, color=GRAY, ha="center",
        rotation=-32)
ax.text(R, -4.75, "$R$（核半径）", fontsize=9, color=GRAY, ha="center")
ax.text(r2, -4.75, "$r_2$", fontsize=9, color=GRAY, ha="center")
ax.text(5.4, -2.7, "经典力学：$E$ 低于垒顶，\nα 不可能逃出", fontsize=9.5,
        color=GRAY, ha="center")
ax.set_xlim(-0.3, 10); ax.set_ylim(-5.2, 9.0)
ax.set_xlabel("到核中心的距离 $r$", fontsize=9.5, color=INK)
ax.set_ylabel("势能 $V(r)$", fontsize=9.5, color=INK)
ax.set_xticks([]); ax.set_yticks([])
style_ax(ax)
fig.tight_layout()
fig.savefig(OUT / "fig_alpha.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ============================================================
# 图6：STM 示意 + 隧穿电流对间距的指数依赖（回扣页）
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 3.1),
                               gridspec_kw={"width_ratios": [1, 1.15]})
# 左：针尖-样品示意
ax1.set_xlim(0, 10); ax1.set_ylim(0, 7); ax1.axis("off")
# 样品表面（带原子起伏）
xs = np.linspace(0.5, 9.5, 400)
surf = 1.2 + 0.35 * np.sin(xs * 2.2) + 0.18 * np.sin(xs * 5.1 + 1.0)
ax1.fill_between(xs, 0, surf, color=TEAL, alpha=0.25)
ax1.plot(xs, surf, color=TEAL, lw=1.6)
ax1.text(5.0, 0.45, "样品表面", fontsize=10, color=TEAL, ha="center")
# 针尖（倒三角）
tip_x = 4.2
tip_y = surf[np.argmin(abs(xs - tip_x))] + 1.3
ax1.fill([tip_x - 1.5, tip_x + 1.5, tip_x], [6.2, 6.2, tip_y],
         color=GRAY, alpha=0.45)
ax1.plot([tip_x - 1.5, tip_x + 1.5, tip_x, tip_x - 1.5],
         [6.2, 6.2, tip_y, 6.2], color=INK, lw=1.4)
ax1.text(6.9, 5.6, "针尖（可尖到单个原子）", fontsize=9.5, color=INK, ha="center")
# 间距标注
ysurf = surf[np.argmin(abs(xs - tip_x))]
ax1.annotate("", xy=(tip_x, tip_y - 0.06), xytext=(tip_x, ysurf + 0.06),
             arrowprops=dict(arrowstyle="<->", color=OCHRE, lw=1.3))
ax1.text(tip_x + 0.55, (tip_y + ysurf) / 2, "$d\\sim 1$ nm", fontsize=10,
         color=OCHRE)
# 电流箭头
ax1.annotate("", xy=(tip_x + 2.6, tip_y + 1.3), xytext=(tip_x + 0.35, tip_y + 0.35),
             arrowprops=dict(arrowstyle="->", color=OCHRE, lw=1.5))
ax1.text(tip_x + 2.75, tip_y + 1.25, "$I$", fontsize=12, color=OCHRE)
ax1.text(5.0, 6.7, "针尖在表面上方扫描，记录隧穿电流", fontsize=10,
         color=GRAY, ha="center")
# 右：I(d) 指数曲线（对数轴）
d = np.linspace(3, 9, 300)   # Å
I = np.exp(-2.0 * (d - 5.0))  # 任意单位，β≈1 Å^-1
ax2.semilogy(d, I, color=TEAL, lw=2.2)
d0 = 5.0
ax2.plot([d0, d0 + 1], [1, 1], "o", ms=6, color=OCHRE, mfc="white", mew=1.6,
         zorder=5)
ax2.annotate("", xy=(d0 + 1, np.exp(-2)), xytext=(d0, 1),
             arrowprops=dict(arrowstyle="->", color=OCHRE, lw=1.2))
ax2.annotate("间距增 1 Å，电流约降至 $1/7$",
             xy=(d0 + 1, np.exp(-2) * 1.6), xytext=(7.15, 0.9),
             fontsize=9.5, color=OCHRE, ha="center",
             arrowprops=dict(arrowstyle="->", color=OCHRE, lw=0.9))
ax2.set_xlabel("针尖–样品间距 $d$（Å）", fontsize=10, color=INK)
ax2.set_ylabel("隧穿电流 $I$（对数）", fontsize=10, color=INK)
ax2.set_xlim(3, 9); ax2.set_ylim(1e-4, 30)
style_ax(ax2)
fig.tight_layout()
fig.savefig(OUT / "fig_stm.png", dpi=200, facecolor=PAPER)
plt.close(fig)

print("done:", sorted(p.name for p in OUT.glob("*.png")))
