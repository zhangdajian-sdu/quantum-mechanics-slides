"""ch1-s1 黑体辐射与普朗克假设 全部插图"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)

INK = "#20242B"
TEAL = "#1F4E5F"
OCHRE = "#C4622D"
GRAY = "#8A8F98"
PAPER = "#FAF8F4"

h = 6.626e-34
k = 1.381e-23
c = 2.998e8

def planck_nu(nu, T):
    """频率表示的普朗克公式（相对强度）"""
    x = h * nu / (k * T)
    return nu**3 / (np.exp(x) - 1)

# ---------------------------------------------------------------- cover
# 竖向题图：三条不同温度的黑体辐射曲线 + 峰值移动箭头
fig, ax = plt.subplots(figsize=(3.4, 5.4))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

nu = np.linspace(1e12, 4.5e14, 500)
for T, col, lw in [(1500, GRAY, 1.2), (2000, TEAL, 1.6), (2500, OCHRE, 1.8)]:
    u = planck_nu(nu, T)
    ax.plot(nu / 1e14, u / u.max() * (0.8 + (T - 1500) / 1000 * 0.5),
            color=col, lw=lw, label=f"T = {T} K")
peaks = []
for T in (1500, 2000, 2500):
    u = planck_nu(nu, T)
    i = u.argmax()
    peaks.append((nu[i] / 1e14, u[i] / u.max() * (0.8 + (T - 1500) / 1000 * 0.5)))
peaks = np.array(peaks)
ax.annotate("", xy=peaks[2] + [0.1, 0.04], xytext=peaks[0] + [0.15, 0.02],
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0,
                            connectionstyle="arc3,rad=-0.25"))
ax.text(2.6, 1.12, "T 升高\n峰值向高频移动", fontsize=8.5, color=INK, ha="center")
ax.legend(frameon=False, fontsize=8.5, loc="upper right", handlelength=1.4)
ax.set_xlabel(r"频率 $\nu$  ($10^{14}$ Hz)", fontsize=9)
ax.set_ylabel(r"$U(T,\nu)$（归一化）", fontsize=9)
ax.set_xlim(0, 4.5)
ax.set_ylim(0, 1.45)
ax.tick_params(labelsize=8, colors=GRAY)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(GRAY)
fig.savefig(OUT / "fig_cover.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------------------------------------------------------------- cavity
# 带小孔的空腔：近似黑体
fig, ax = plt.subplots(figsize=(6.4, 4.6))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

# 炉体
ax.add_patch(Rectangle((0.5, 0.6), 5.0, 3.6, facecolor="#E8E4DA",
                       edgecolor=INK, lw=1.6))
ax.add_patch(Rectangle((1.0, 1.1), 4.0, 2.6, facecolor="#3A3F4A",
                       edgecolor=INK, lw=1.2))
# 小孔
ax.add_patch(Rectangle((1.0, 2.35), 0.09, 0.3, facecolor=PAPER, edgecolor="none"))
# 入射光与多次反射
ray = [(0.0, 3.05), (1.04, 2.52), (4.9, 3.4), (1.2, 3.55), (4.85, 1.5), (1.3, 1.2)]
for (x0, y0), (x1, y1) in zip(ray[:-1], ray[1:]):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.5))
ax.text(-0.05, 3.12, "入射光", fontsize=10, color=OCHRE, ha="left")
ax.text(2.9, 2.35, "内壁多次反射吸收", fontsize=10.5, color="#E8E4DA", ha="center")
ax.text(0.62, 4.42, "空腔（炉壁保持温度 T）", fontsize=10.5, color=INK, ha="left")
ax.text(1.16, 2.68, "小孔", fontsize=9.5, color="#E8E4DA", ha="left")
# 小孔辐射
for y1 in (1.55, 1.85, 2.15):
    ax.annotate("", xy=(0.0, y1), xytext=(0.98, 2.42),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.5))
ax.text(-0.05, 1.18, "黑体辐射", fontsize=10, color=TEAL, ha="left")

ax.set_xlim(-0.2, 5.8)
ax.set_ylim(0.5, 4.7)
ax.axis("off")
fig.savefig(OUT / "fig_cavity.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------------------------------------------------------------- spectrum
# 实验曲线：不同温度 U(T,nu)
fig, ax = plt.subplots(figsize=(7.6, 4.4))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

nu = np.linspace(1e12, 6e14, 600)
umax = planck_nu(nu, 2500).max()
for T, col in [(1500, GRAY), (2000, TEAL), (2500, OCHRE)]:
    u = planck_nu(nu, T)
    ax.plot(nu / 1e14, u / umax * 4.0, color=col, lw=1.8, label=f"T = {T} K")
    i = u.argmax()
    ax.plot(nu[i] / 1e14, u[i] / umax * 4.0, "o", ms=5, color=col)
ax.annotate("峰值随 T 升高向高频移动\n（维恩位移）", xy=(2.6, 2.6),
            xytext=(3.2, 3.3), fontsize=10, color=INK,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0))
ax.set_xlabel(r"频率 $\nu$  ($10^{14}$ Hz)", fontsize=11)
ax.set_ylabel(r"$U(T,\nu)$（任意单位）", fontsize=11)
ax.set_xlim(0, 6)
ax.set_ylim(0, 4.4)
ax.legend(frameon=False, fontsize=10, loc="upper right")
ax.tick_params(labelsize=9.5, colors=GRAY)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(GRAY)
fig.savefig(OUT / "fig_spectrum.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------------------------------------------------------------- compare
# 固定温度：普朗克 vs 瑞利-金斯 vs 维恩（对数纵轴）
fig, ax = plt.subplots(figsize=(7.6, 4.4))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

x = np.linspace(0.15, 9, 600)
pl = x**3 / (np.exp(x) - 1)
rj = x**2
wn = x**3 * np.exp(-x)
ax.plot(x, rj, color=GRAY, lw=1.8, ls="--", label=r"瑞利–金斯  $x^2$")
ax.plot(x, wn, color=OCHRE, lw=1.8, ls="-.", label=r"维恩  $x^3\mathrm{e}^{-x}$")
ax.plot(x, pl, color=TEAL, lw=2.4, label=r"实验（普朗克公式）  $x^3/(\mathrm{e}^x-1)$")
ax.set_yscale("log")
ax.annotate("「紫外灾难」：高频端\n经典理论单调发散", xy=(6.5, 42), xytext=(3.4, 60),
            fontsize=10.5, color=INK,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0))
ax.annotate("低频端：瑞利–金斯\n与实验一致", xy=(0.7, 0.5), xytext=(0.5, 12),
            fontsize=10.5, color=INK,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0))
ax.annotate("维恩公式在低频端\n偏离实验", xy=(1.35, 0.42), xytext=(2.1, 0.03),
            fontsize=10.5, color=INK,
            arrowprops=dict(arrowstyle="->", color=OCHRE, lw=1.0))
ax.set_xlabel(r"$x = h\nu / kT$（无量纲频率）", fontsize=11)
ax.set_ylabel(r"$U$（任意单位，对数刻度）", fontsize=11)
ax.set_xlim(0, 9)
ax.set_ylim(1e-2, 3e2)
ax.legend(frameon=False, fontsize=10, loc="lower right")
ax.tick_params(labelsize=9.5, colors=GRAY)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(GRAY)
fig.savefig(OUT / "fig_compare.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------------------------------------------------------------- kspace
# 模式计数示意：n 空间格点与 1/8 球壳（二维示意）
fig, ax = plt.subplots(figsize=(5.6, 5.0))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

N = 12
gx, gy = np.meshgrid(np.arange(1, N + 1), np.arange(1, N + 1))
r = np.sqrt(gx**2 + gy**2)
inner = (r >= 8.5) & (r <= 9.6)
ax.scatter(gx[~inner], gy[~inner], s=26, color=TEAL, alpha=0.45)
ax.scatter(gx[inner], gy[inner], s=30, color=OCHRE)
th = np.linspace(0, np.pi / 2, 200)
ax.plot(8.5 * np.cos(th), 8.5 * np.sin(th), color=INK, lw=1.4)
ax.plot(9.6 * np.cos(th), 9.6 * np.sin(th), color=INK, lw=1.4)
ax.plot([8.5, 9.6], [0.35, 0.35], color="none")
ax.text(5.1, 9.6, r"格点 $(n_x,n_y,n_z)$，每点对应一个驻波模式", fontsize=10, color=TEAL)
ax.text(10.3, 6.4, r"壳层内的格点数" + "\n" + r"$\approx \frac{1}{8}\times 4\pi n^2\,\mathrm{d}n$", fontsize=10, color=OCHRE)
ax.set_xlim(0, 13)
ax.set_ylim(0, 12.5)
ax.set_xlabel(r"$n_x$", fontsize=11)
ax.set_ylabel(r"$n_y$", fontsize=11)
ax.tick_params(labelsize=9, colors=GRAY)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(GRAY)
ax.set_aspect("equal")
fig.savefig(OUT / "fig_kspace.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

print("done:", [p.name for p in OUT.glob("*.png")])
