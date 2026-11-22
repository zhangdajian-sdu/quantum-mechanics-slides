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
HAIR = "#E2DFD8"

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print("saved", name)


# ---------- 封面：过程越短，能量越「模糊」（teal 底） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

x = np.linspace(-3, 3, 800)
for g, a, lb in [(1.0, 1.0, None), (3.0, 0.55, None)]:
    y = (g ** 2 / 4.0) / (x ** 2 + g ** 2 / 4.0)
    ax.plot(x, y * 0.9 + 0.10, color="#FAF8F4", lw=1.8, alpha=a)

ax.axhline(0.55, color="#E8B48C", lw=1.2, ls="--", alpha=0.9, xmax=0.72, xmin=0.28)
ax.annotate("", xy=(0.5, 0.55), xytext=(-0.5, 0.55),
            arrowprops=dict(arrowstyle="<|-|>", color="#E8B48C", lw=1.6))
ax.text(0.0, 0.61, "宽度 Γ", color="#E8B48C", fontsize=12, ha="center")

ax.text(0.0, 1.52, "过程越短，", color="#FAF8F4", fontsize=17, ha="center", weight="bold")
ax.text(0.0, 1.38, "能量越「模糊」", color="#FAF8F4", fontsize=17, ha="center", weight="bold")
ax.text(0.0, 1.21, "$\\Delta E\\,\\Delta t\\approx\\hbar$", color="#E8B48C", fontsize=15, ha="center")
ax.text(0.0, 0.01, "同一类峰：微扰时间、运动过程、粒子寿命", color="#FFFFFF99", fontsize=11, ha="center")
ax.set_xlim(-3.2, 3.2)
ax.set_ylim(-0.06, 1.66)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 图 7.3 型：W 随 E_m−E_k−ħω 的分布（sin² 峰） ----------
fig, ax = plt.subplots(figsize=(8.4, 5.0), facecolor=PAPER)
ax.set_facecolor(PAPER)

# x 以 h/t1 = 2πħ/t1 为单位；u = π x
x = np.linspace(-3.2, 3.2, 2000)
for r, c, lb in [(1.0, "#5B7B8A", "微扰时间 t"), (3.0, TEAL, "微扰时间 3t")]:
    u = np.pi * x * r
    y = np.where(np.abs(u) < 1e-9, 1.0, np.sin(u) ** 2 / u ** 2)
    ax.plot(x, y * r ** 2, color=c, lw=2.0 if r > 1 else 1.6, label=lb)

for sgn in (-1, 1):
    ax.plot([sgn, sgn], [0, 1.7], color=GRAY, lw=1.0, ls=":")
ax.annotate("", xy=(1.0, 1.35), xytext=(-1.0, 1.35),
            arrowprops=dict(arrowstyle="<|-|>", color=OCHRE, lw=1.5))
ax.text(0, 1.9, "主峰宽度 $\\approx 2h/t$", fontsize=12.5, color=OCHRE, ha="center")

ax.set_xlabel(r"末态能量偏离 $E_m-(E_k+\hbar\omega)$（单位：$h/t$）", fontsize=12.5, color=INK)
ax.set_ylabel(r"跃迁几率 $W_{k\to m}(t)$", fontsize=12.5, color=INK)
ax.set_xticks([-1, 0, 1])
ax.set_xticklabels(["$-h/t$", "0\n（共振：$E_m=E_k+\\hbar\\omega$）", "$+h/t$"], fontsize=11)
ax.set_yticks([])
ax.set_xlim(-3.2, 3.2); ax.set_ylim(-1.05, 10.5)
ax.tick_params(colors=GRAY, labelsize=10)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(HAIR)
ax.legend(frameon=False, fontsize=11.5, loc="upper right")
ax.set_title("微扰只作用了时间 t：末态能量集中在主峰内（图 7.3 的曲线）", fontsize=13.5, color=INK, pad=8)
save(fig, "fig_peak.png")


# ---------- 图 7.4 型：不稳定态的洛伦兹能量分布 ----------
fig, ax = plt.subplots(figsize=(8.4, 5.0), facecolor=PAPER)
ax.set_facecolor(PAPER)

x = np.linspace(-3.0, 3.0, 1200)
y = (1.0 / 4.0) / (x ** 2 + 1.0 / 4.0)  # Γ = 1, 峰值 1
ax.plot(x, y, color=TEAL, lw=2.2)
ax.axhline(0.5, color=GRAY, lw=1.1, ls="--", xmax=0.667, xmin=0.333)
ax.plot([-0.5, 0.5], [0.5, 0.5], color=OCHRE, lw=2.2)
for sgn in (-1, 1):
    ax.plot([sgn * 0.5, sgn * 0.5], [0, 0.5], color=OCHRE, lw=1.2, ls=":")
ax.annotate("", xy=(0.5, 0.44), xytext=(-0.5, 0.44),
            arrowprops=dict(arrowstyle="<|-|>", color=OCHRE, lw=1.4))
ax.text(0, 0.30, "半高全宽 = Γ", fontsize=12.5, color=OCHRE, ha="center")
ax.text(0.06, 0.86, "最可几能量 $E_0$", fontsize=12.5, color=INK)
ax.plot([0], [1.0], "o", color=OCHRE, ms=6)

ax.set_xlabel(r"能量 $E$（以 $E_0$ 为中心，单位：Γ）", fontsize=12.5, color=INK)
ax.set_ylabel(r"能量分布几率密度 $P(E)$", fontsize=12.5, color=INK)
ax.set_xticks([-0.5, 0, 0.5])
ax.set_xticklabels(["$E_0-\\Gamma/2$", "$E_0$", "$E_0+\\Gamma/2$"], fontsize=11)
ax.set_yticks([])
ax.set_xlim(-3.0, 3.0); ax.set_ylim(0, 1.12)
ax.tick_params(colors=GRAY, labelsize=10)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(HAIR)
ax.set_title("不稳定态没有单一能量：洛伦兹型分布（图 7.4 的曲线）", fontsize=13.5, color=INK, pad=8)
save(fig, "fig_lorentz.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
