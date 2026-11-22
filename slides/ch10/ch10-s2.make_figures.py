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

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print("saved", name)


# ---------- 封面：平面波的分波（teal 底，竖版） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

# 入射平面波
xs = np.linspace(-4.3, -1.35, 300)
for y0 in np.linspace(-3.6, 3.6, 8):
    ax.plot(xs, y0 + 0.15 * np.sin(2.6 * xs), color="#FAF8F4", lw=1.0, alpha=0.75)

# 中心与分波环
ax.plot(0, 0, "o", ms=12, color="#E8B48C", mec="#FAF8F4", mew=1.4)
for i, r in enumerate([0.95, 1.85, 2.75]):
    circ = plt.Circle((0, 0), r, fill=False, color="#FAF8F4",
                      lw=1.2, alpha=0.85 - i * 0.2)
    ax.add_patch(circ)
    ax.text(r / np.sqrt(2) + 0.06, r / np.sqrt(2) + 0.10, f"l={i}",
            color="#FAF8F4", fontsize=13, alpha=0.95 - i * 0.15)

# 各方向出射箭头
for ang in [15, 45, 75, 105, 135, 165]:
    th = np.deg2rad(ang)
    ax.annotate("", xy=(3.9 * np.cos(th), 3.9 * np.sin(th)),
                xytext=(2.75 * np.cos(th), 2.75 * np.sin(th)),
                arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=1.3, alpha=0.9))
    ax.annotate("", xy=(3.9 * np.cos(-th), 3.9 * np.sin(-th)),
                xytext=(2.75 * np.cos(-th), 2.75 * np.sin(-th)),
                arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=1.3, alpha=0.9))

ax.text(-4.0, 3.95, r"$\mathrm{e}^{ikz}=\sum_l(\cdots)\,j_l(kr)Y_{l0}$",
        color="#FAF8F4", fontsize=13)
ax.text(0, -4.5, r"$f(\theta)=\dfrac{1}{k}\sum_l(2l+1)\,\mathrm{e}^{i\delta_l}\sin\delta_l\,P_l(\cos\theta)$",
        color="#E8B48C", fontsize=14, ha="center")

ax.set_xlim(-4.6, 4.6)
ax.set_ylim(-5.0, 4.5)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 相移：有/无势场的 s 波径向波函数 ----------
a = 3.0
k = 1.0
beta = 1.5  # 吸引势阱内波数更大
r = np.linspace(1e-3, 13, 1600)
u_in = np.sin(beta * r)
phi = np.arctan2(k * np.sin(beta * a), beta * np.cos(beta * a))
if phi < 0:
    phi += np.pi
C = np.sin(beta * a) / np.sin(phi)
d0 = phi - k * a  # 相移
u_out = C * np.sin(k * r + d0)
u = np.where(r <= a, u_in, u_out)
u_free = C * np.sin(k * r)

fig, ax = plt.subplots(figsize=(7.8, 3.4), facecolor=PAPER)
ax.set_facecolor(PAPER)
ax.axvspan(0, a, color=TEAL, alpha=0.08)
ax.text(a / 2, 1.28, "势场区 $r<a$", ha="center", fontsize=11, color=TEAL)
ax.plot(r, u_free, color=GRAY, lw=1.6, ls="--", label=r"无势场：$\sin kr$")
ax.plot(r, u, color=TEAL, lw=2.2, label=r"有势场：$\sin(kr+\delta_0)$")
ax.axhline(0, color=INK, lw=0.8)
ax.axvline(a, color=GRAY, lw=0.8, ls=":")

# 在远处标出相移对应的零点位移
n = 3
r0_free = n * np.pi / k
r0_shift = (n * np.pi - d0) / k
ax.annotate("", xy=(r0_shift, -1.32), xytext=(r0_free, -1.32),
            arrowprops=dict(arrowstyle="<->", color=OCHRE, lw=1.4))
ax.text((r0_free + r0_shift) / 2, -1.62, r"$\delta_0/k$", color=OCHRE,
        fontsize=13, ha="center")

ax.set_xlim(0, 13); ax.set_ylim(-1.85, 2.15)
ax.set_xticks([]); ax.set_yticks([])
ax.legend(fontsize=11, loc="upper right", frameon=False)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
save(fig, "fig_shift.png")


# ---------- 低能判据：只有 b<a 的粒子被散射（仿教材图 10.2） ----------
fig, ax = plt.subplots(figsize=(7.4, 3.6), facecolor=PAPER)
ax.set_facecolor(PAPER)

a = 1.0
circ = plt.Circle((0, 0), a, color=TEAL, alpha=0.12, zorder=1)
ax.add_patch(circ)
ax.plot(0, 0, "o", ms=9, color=OCHRE, zorder=4)
ax.text(0.14, -0.34, "靶", fontsize=11, color=OCHRE)
ax.annotate("势作用半径 a", xy=(0.5, 0.87), xytext=(1.25, 2.25),
            fontsize=11, color=TEAL,
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=0.9))

for b in [0.35, 0.75, 1.35, 1.75]:
    hit = b < a
    c = TEAL if hit else GRAY
    al = 1.0 if hit else 0.55
    ax.annotate("", xy=(-np.sqrt(max(a ** 2 - b ** 2, 0)) - 0.02, b), xytext=(-3.9, b),
                arrowprops=dict(arrowstyle="-|>", color=c, lw=1.5, alpha=al))
    if hit:
        th = np.deg2rad(150 - 90 * b / a)
        ax.plot([0, 2.6 * np.cos(th)], [0, b + 2.6 * np.sin(th) * 0.5],
                color=TEAL, lw=1.5)
    else:
        ax.plot([-0.05, 3.4], [b, b], color=GRAY, lw=1.5, alpha=0.55)

# 角动量标注
ax.annotate("", xy=(-2.6, 0.75), xytext=(-2.6, 0),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=1.2))
ax.text(-2.52, 0.3, "b", fontsize=13, color=INK, style="italic")
ax.axhline(0, color=GRAY, lw=0.8, ls=(0, (4, 3)))
ax.text(-3.85, 2.2, r"轨道角动量 $L=pb$；只有 $b<a$ 才发生散射", fontsize=12, color=INK)

ax.set_xlim(-4.1, 3.6)
ax.set_ylim(-0.8, 2.6)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_lowE.png")


# ---------- 散射长度：零能 s 波渐近线的截距（示意） ----------
fig, ax = plt.subplots(figsize=(7.4, 3.4), facecolor=PAPER)
ax.set_facecolor(PAPER)

aw = 2.0          # 势场区边界（示意）
a0 = 0.75         # 散射长度 = 渐近线在 r 轴上的截距
slope = 0.8       # 渐近直线斜率
r_in = np.linspace(0, aw, 300)
u_in = 0.2 * r_in + 0.15 * r_in ** 2            # 内部曲线（示意，u(0)=0）
r_out = np.linspace(aw, 6.4, 200)
u_out = 1.0 + slope * (r_out - aw)              # 外部零能解：直线

ax.axhline(0, color=INK, lw=0.9)
ax.axvspan(0, aw, color=TEAL, alpha=0.08)
ax.text(aw / 2, 3.6, "势场区", ha="center", fontsize=11, color=TEAL)
ax.plot(r_in, u_in, color=TEAL, lw=2.2)
ax.plot(r_out, u_out, color=TEAL, lw=2.2)
# 渐近线反向延长（虚线）交 r 轴于 a0
ax.plot([a0, aw], [0, 1.0], color=OCHRE, lw=1.4, ls="--")
ax.plot(a0, 0, "o", ms=7, color=OCHRE)
ax.annotate("", xy=(a0, -0.42), xytext=(0, -0.42),
            arrowprops=dict(arrowstyle="<->", color=OCHRE, lw=1.3))
ax.text(a0 / 2, -0.78, r"$a_0$", color=OCHRE, fontsize=14, ha="center")
ax.text(4.35, 1.15, r"$u(r)\,(E\to0)\;=A\left(1-\dfrac{r}{a_0}\right)$",
        fontsize=13, color=INK)
ax.text(6.45, 5.35, r"$u(r)$", fontsize=12, color=INK)
ax.text(6.45, -0.3, r"$r$", fontsize=12, color=INK)
ax.annotate("", xy=(6.5, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9))
ax.set_xlim(-0.35, 6.8)
ax.set_ylim(-1.1, 5.6)
ax.set_xticks([]); ax.set_yticks([])
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
save(fig, "fig_scatlen.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
