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


# ---------- 封面：两粒子对撞，质心匀速前行（teal 底，竖版） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

# 碰撞前：m1 向右，m2 向左（质心系）
ax.plot(-2.6, 1.5, "o", ms=12, color="#FAF8F4")
ax.plot(2.6, 1.5, "o", ms=17, color="#E8B48C")
ax.annotate("", xy=(-0.9, 1.5), xytext=(-2.2, 1.5),
            arrowprops=dict(arrowstyle="-|>", color="#FAF8F4", lw=1.8))
ax.annotate("", xy=(0.9, 1.5), xytext=(2.1, 1.5),
            arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=1.8))
ax.text(-2.6, 2.0, r"$m_1$", color="#FAF8F4", fontsize=14, ha="center")
ax.text(2.6, 2.05, r"$m_2$", color="#E8B48C", fontsize=14, ha="center")
ax.text(-1.7, 1.85, r"$u_1$", color="#FAF8F4", fontsize=12)
ax.text(1.55, 1.85, r"$u_2$", color="#E8B48C", fontsize=12)

# 碰撞点
ax.plot(0, 1.5, "o", ms=5, color="#FAF8F4", alpha=0.7)

# 碰撞后：沿 ±θ 离去
th = np.deg2rad(38)
ax.annotate("", xy=(2.9 * np.cos(th), 1.5 + 2.9 * np.sin(th)), xytext=(0.4, 1.8),
            arrowprops=dict(arrowstyle="-|>", color="#FAF8F4", lw=1.8))
ax.annotate("", xy=(-2.9 * np.cos(th), 1.5 - 2.9 * np.sin(th)), xytext=(-0.4, 1.2),
            arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=1.8))
ax.plot([0, 2.2], [1.5, 1.5], color="#FAF8F4", lw=0.9, ls=(0, (3, 3)), alpha=0.6)
arc = np.linspace(0, th, 60)
ax.plot(1.5 * np.cos(arc), 1.5 + 1.5 * np.sin(arc), color="#FAF8F4", lw=1.1, alpha=0.85)
ax.text(1.85, 2.15, r"$\theta$", color="#FAF8F4", fontsize=14)

ax.text(0, -1.6, "质心系：碰撞前后速率不变，只改方向", color="#FAF8F4",
        fontsize=13.5, ha="center")
ax.text(0, -2.5, r"$\tan\theta_l=\dfrac{m_2\sin\theta}{m_1+m_2\cos\theta}$",
        color="#E8B48C", fontsize=15, ha="center")

ax.set_xlim(-4.4, 4.4)
ax.set_ylim(-4.9, 4.0)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 质心系碰撞图景（仿教材图 10.4） ----------
fig, ax = plt.subplots(figsize=(7.6, 3.0), facecolor=PAPER)
ax.set_facecolor(PAPER)

ax.axhline(0, color=GRAY, lw=0.9, ls=(0, (4, 3)))
# 入射
ax.plot(-2.9, 0, "o", ms=11, color=TEAL)
ax.plot(2.9, 0, "o", ms=15, color=OCHRE)
ax.annotate("", xy=(-0.95, 0), xytext=(-2.45, 0),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.8))
ax.annotate("", xy=(0.95, 0), xytext=(2.35, 0),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.8))
ax.text(-2.9, 0.28, r"$m_1$", fontsize=12, color=TEAL, ha="center")
ax.text(2.9, 0.3, r"$m_2$", fontsize=12, color=OCHRE, ha="center")
ax.text(-1.75, 0.24, r"$u_1$", fontsize=11.5, color=TEAL)
ax.text(1.6, 0.24, r"$u_2$", fontsize=11.5, color=OCHRE)

# 出射
th = np.deg2rad(52)
ax.plot(0, 0, "o", ms=5, color=INK)
ax.annotate("", xy=(2.7 * np.cos(th), 2.7 * np.sin(th)), xytext=(0.35, 0.22),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.8))
ax.annotate("", xy=(-2.7 * np.cos(th), -2.7 * np.sin(th)), xytext=(-0.35, -0.22),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.8))
arc = np.linspace(0, th, 60)
ax.plot(1.2 * np.cos(arc), 1.2 * np.sin(arc), color=INK, lw=1.1)
ax.text(1.5, 0.62, r"$\theta$", fontsize=13, color=INK)

ax.set_xlim(-3.4, 3.4)
ax.set_ylim(-2.0, 2.2)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cm.png")


# ---------- 速度合成：V1' = u1' + VM（仿教材图 10.5） ----------
fig, ax = plt.subplots(figsize=(6.8, 3.6), facecolor=PAPER)
ax.set_facecolor(PAPER)

th = np.deg2rad(58)
VM = 1.6
u1 = 2.4
# VM 沿 x 轴
ax.annotate("", xy=(VM, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=2.0))
ax.text(VM / 2, -0.3, r"$V_M$", fontsize=13.5, color=GRAY, ha="center")
# u1' 从 VM 末端出发，与 x 轴成 θ
tip = (VM + u1 * np.cos(th), u1 * np.sin(th))
ax.annotate("", xy=tip, xytext=(VM, 0),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.0))
ax.text(VM + u1 * np.cos(th) * 0.55 + 0.1, u1 * np.sin(th) * 0.55,
        r"$u_1^{\prime}$", fontsize=13.5, color=OCHRE)
# V1' 从原点
ax.annotate("", xy=tip, xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.2))
ax.text(tip[0] * 0.44 - 0.15, tip[1] * 0.55, r"$V_1^{\prime}$", fontsize=13.5, color=TEAL)
# 角度标注
thl = np.arctan2(tip[1], tip[0])
arc1 = np.linspace(0, thl, 60)
ax.plot(0.9 * np.cos(arc1), 0.9 * np.sin(arc1), color=TEAL, lw=1.2)
ax.text(1.02, 0.3, r"$\theta_l$", fontsize=13, color=TEAL)
arc2 = np.linspace(0, th, 60)
ax.plot(VM + 0.85 * np.cos(arc2), 0.85 * np.sin(arc2), color=OCHRE, lw=1.2)
ax.text(VM + 1.0, 0.26, r"$\theta$", fontsize=13, color=OCHRE)
ax.plot([VM, tip[0] + 0.6], [0, 0], color=GRAY, lw=0.8, ls=(0, (3, 3)))

ax.text(0.1, 2.75, r"$\tan\theta_l=\dfrac{u_1\sin\theta}{V_M+u_1\cos\theta}$",
        fontsize=13.5, color=INK)

ax.set_xlim(-0.5, 4.6)
ax.set_ylim(-0.7, 3.1)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_velocity.png")


# ---------- θ_l 与 θ 的关系：不同质量比 ----------
fig, ax = plt.subplots(figsize=(7.2, 3.4), facecolor=PAPER)
ax.set_facecolor(PAPER)

th = np.linspace(0, np.pi, 400)
for ratio, c, lab in [(0.2, TEAL, r"$m_1/m_2=0.2$"),
                      (1.0, OCHRE, r"$m_1/m_2=1$"),
                      (3.0, GRAY, r"$m_1/m_2=3$")]:
    thl = np.arctan2(np.sin(th), ratio + np.cos(th))
    ax.plot(np.rad2deg(th), np.rad2deg(thl), color=c, lw=2.2, label=lab)

ax.plot([0, 180], [0, 180], color=INK, lw=0.8, ls=":", alpha=0.5)
ax.set_xlabel(r"质心系散射角 $\theta$（度）", fontsize=11, color=INK)
ax.set_ylabel(r"实验室系散射角 $\theta_l$（度）", fontsize=11, color=INK)
ax.legend(fontsize=11, loc="upper left", frameon=False)
ax.set_xlim(0, 180); ax.set_ylim(0, 180)
ax.tick_params(labelsize=10, colors=INK)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
save(fig, "fig_theta.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
