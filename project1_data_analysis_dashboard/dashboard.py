"""
dashboard.py
------------
Generates a multi-panel visual dashboard (PNG) from
the cleaned sales dataset using Matplotlib only.
Saved to outputs/dashboard.png
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch

# ── CONFIG ───────────────────────────────────────────────
CLEAN_PATH = "data/cleaned_data.csv"
OUT_PATH   = "outputs/dashboard.png"
os.makedirs("outputs", exist_ok=True)

COLORS = {
    "bg":        "#0f0f0f",
    "panel":     "#1a1a2e",
    "accent":    "#e94560",
    "accent2":   "#f5a623",
    "accent3":   "#4ecca3",
    "text":      "#e0e0e0",
    "muted":     "#888888",
    "bars":      ["#e94560", "#f5a623", "#4ecca3", "#7b68ee"],
}


def load(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["Order_Date"])
    df["Revenue"]    = df["Sales"] * df["Quantity"]
    df["Net_Profit"] = df["Profit"] * df["Quantity"]
    return df


def kpi_card(ax, title: str, value: str, color: str) -> None:
    ax.set_facecolor(COLORS["panel"])
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor(color)
        spine.set_linewidth(2)
    ax.text(0.5, 0.62, value, ha="center", va="center",
            fontsize=22, fontweight="bold", color=color,
            transform=ax.transAxes)
    ax.text(0.5, 0.25, title, ha="center", va="center",
            fontsize=9, color=COLORS["muted"],
            transform=ax.transAxes)


def plot_bar_h(ax, labels, values, color, title):
    ax.set_facecolor(COLORS["panel"])
    bars = ax.barh(labels, values, color=color, height=0.55)
    ax.set_title(title, color=COLORS["text"], fontsize=10, pad=8)
    ax.tick_params(colors=COLORS["text"], labelsize=8)
    ax.xaxis.label.set_color(COLORS["muted"])
    for spine in ax.spines.values():
        spine.set_edgecolor("#333")
    ax.set_facecolor(COLORS["panel"])
    ax.invert_yaxis()
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + max(values) * 0.01, bar.get_y() + bar.get_height() / 2,
                f"₹{val:,.0f}", va="center", color=COLORS["text"], fontsize=7.5)
    ax.set_xlim(0, max(values) * 1.22)
    ax.grid(axis="x", color="#333", linewidth=0.5, linestyle="--")


def plot_line(ax, x, y, color, title):
    ax.set_facecolor(COLORS["panel"])
    ax.plot(x, y, color=color, linewidth=2.5, marker="o",
            markersize=5, markerfacecolor=COLORS["bg"])
    ax.fill_between(x, y, alpha=0.15, color=color)
    ax.set_title(title, color=COLORS["text"], fontsize=10, pad=8)
    ax.tick_params(colors=COLORS["text"], labelsize=8)
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=30, ha="right", fontsize=7)
    for spine in ax.spines.values():
        spine.set_edgecolor("#333")
    ax.grid(color="#333", linewidth=0.5, linestyle="--")


def plot_pie(ax, labels, values, title):
    ax.set_facecolor(COLORS["panel"])
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct="%1.1f%%",
        colors=COLORS["bars"], startangle=140,
        wedgeprops=dict(edgecolor=COLORS["bg"], linewidth=1.5),
        textprops=dict(color=COLORS["text"], fontsize=8),
    )
    for at in autotexts:
        at.set_color(COLORS["bg"])
        at.set_fontsize(8)
    ax.set_title(title, color=COLORS["text"], fontsize=10, pad=8)


def build_dashboard(df: pd.DataFrame) -> None:
    fig = plt.figure(figsize=(18, 11), facecolor=COLORS["bg"])
    fig.suptitle("Sales Analytics Dashboard",
                 fontsize=22, fontweight="bold",
                 color=COLORS["text"], y=0.97)

    gs = gridspec.GridSpec(3, 4, figure=fig,
                           hspace=0.55, wspace=0.4,
                           left=0.05, right=0.97,
                           top=0.90, bottom=0.06)

    # ── KPI CARDS (row 0) ──────────────────────────────────
    kpi_data = [
        ("Total Revenue",    f"₹{df['Revenue'].sum():,.0f}",    COLORS["accent"]),
        ("Total Profit",     f"₹{df['Net_Profit'].sum():,.0f}", COLORS["accent2"]),
        ("Profit Margin",    f"{(df['Net_Profit'].sum()/df['Revenue'].sum()*100):.1f}%",
                                                                 COLORS["accent3"]),
        ("Total Orders",     str(df["Order_ID"].nunique()),      "#7b68ee"),
    ]
    for i, (title, val, col) in enumerate(kpi_data):
        ax = fig.add_subplot(gs[0, i])
        kpi_card(ax, title, val, col)

    # ── TOP PRODUCTS BY REVENUE (row 1, col 0-1) ──────────
    ax2 = fig.add_subplot(gs[1, :2])
    top = (df.groupby("Product")["Revenue"].sum()
           .sort_values(ascending=False).head(6))
    plot_bar_h(ax2, top.index.tolist(), top.values.tolist(),
               COLORS["accent"], "Top 6 Products by Revenue")

    # ── REVENUE BY CATEGORY PIE (row 1, col 2) ────────────
    ax3 = fig.add_subplot(gs[1, 2])
    cat = df.groupby("Category")["Revenue"].sum()
    plot_pie(ax3, cat.index.tolist(), cat.values.tolist(),
             "Revenue by Category")

    # ── REGIONAL PERFORMANCE BAR (row 1, col 3) ───────────
    ax4 = fig.add_subplot(gs[1, 3])
    reg = (df.groupby("Region")["Revenue"].sum()
           .sort_values(ascending=False))
    plot_bar_h(ax4, reg.index.tolist(), reg.values.tolist(),
               COLORS["accent3"], "Regional Revenue")

    # ── MONTHLY REVENUE TREND (row 2, col 0-2) ────────────
    ax5 = fig.add_subplot(gs[2, :3])
    monthly = (df.groupby(["Month_Num", "Month"])["Revenue"]
               .sum().reset_index().sort_values("Month_Num"))
    plot_line(ax5, monthly["Month"].tolist(),
              monthly["Revenue"].tolist(),
              COLORS["accent2"], "Monthly Revenue Trend")

    # ── PROFIT MARGIN BY REGION (row 2, col 3) ────────────
    ax6 = fig.add_subplot(gs[2, 3])
    pm = (df.groupby("Region")
          .apply(lambda x: x["Net_Profit"].sum() / x["Revenue"].sum() * 100)
          .sort_values(ascending=False))
    ax6.set_facecolor(COLORS["panel"])
    bars = ax6.bar(pm.index, pm.values,
                   color=COLORS["bars"][:len(pm)], width=0.55)
    ax6.set_title("Profit Margin % by Region",
                  color=COLORS["text"], fontsize=10, pad=8)
    ax6.tick_params(colors=COLORS["text"], labelsize=8)
    for spine in ax6.spines.values():
        spine.set_edgecolor("#333")
    ax6.grid(axis="y", color="#333", linewidth=0.5, linestyle="--")
    for bar, val in zip(bars, pm.values):
        ax6.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.4,
                 f"{val:.1f}%", ha="center",
                 color=COLORS["text"], fontsize=8)

    plt.savefig(OUT_PATH, dpi=150, bbox_inches="tight",
                facecolor=COLORS["bg"])
    print(f"[INFO] Dashboard saved to '{OUT_PATH}'")
    plt.close()


if __name__ == "__main__":
    df = load(CLEAN_PATH)
    build_dashboard(df)
