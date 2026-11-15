"""
Generate every image in assets/ from the recorded results (docs/outputs/results.json).
Run scripts/run_scenarios.py first, then:  python scripts/generate_visuals.py
"""
import glob
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                    # noqa: E402
from matplotlib import font_manager                                # noqa: E402
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)
R = json.load(open(os.path.join(ROOT, "docs", "outputs", "results.json"), encoding="utf-8"))
K = R["constants"]

# ---- fonts: Inter if installed, otherwise matplotlib's DejaVu Sans ----------
for f in glob.glob("/usr/share/fonts/**/Inter-*.otf", recursive=True):
    font_manager.fontManager.addfont(f)
plt.rcParams["font.family"] = ["Inter", "DejaVu Sans"]

# ---- palette ----------------------------------------------------------------
INK, PAPER, MUTED = "#10223A", "#F4F7FA", "#5B6B7F"
SAPPHIRE, JADE = "#2F5FD0", "#0E9F7E"       # scholarship / pharmacy identities
OK, BAD, WARN = "#1E9E6A", "#D64545", "#E8A317"
LINE = "#C9D3DE"


def save(fig, name, dpi=150):
    fig.savefig(os.path.join(ASSETS, name), dpi=dpi, facecolor=fig.get_facecolor(),
                bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("wrote", name)


# =============================================================================
# 1. Banner
# =============================================================================
def banner():
    import numpy as np
    fig = plt.figure(figsize=(16, 4.2), facecolor=INK)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 42)
    ax.axis("off")
    # faint grid (drawn first, below everything)
    for x in range(0, 161, 8):
        ax.plot([x, x], [0, 42], color="#1B3350", lw=0.6, zorder=0)
    for y in range(0, 43, 8):
        ax.plot([0, 160], [y, y], color="#1B3350", lw=0.6, zorder=0)

    ax.text(8, 28, "Python Conditions & Loops", color="white", fontsize=40,
            fontweight="bold", va="center", zorder=5)
    ax.text(8, 19, "Two console applications that decide with if / elif / else", color="#B8C7D9",
            fontsize=17, va="center", zorder=5)
    ax.text(8, 14, "and repeat with for loops, counters and accumulators.", color="#B8C7D9",
            fontsize=17, va="center", zorder=5)
    for x, label, col in [(8, "Task 1  Scholarship Eligibility", SAPPHIRE),
                          (56, "Task 2  Pharmacy Inventory", JADE)]:
        ax.add_patch(FancyBboxPatch((x, 4), 43, 5.2, boxstyle="round,pad=0,rounding_size=1.2",
                                    fc=col, ec="none", zorder=3))
        ax.text(x + 21.5, 6.6, label, color="white", fontsize=13.5, fontweight="bold",
                ha="center", va="center", zorder=5)

    # right motif: decision diamond -> outcome, with a loop underneath
    cx, cy = 112, 27
    ax.add_patch(Polygon([[cx, cy + 11], [cx + 13, cy], [cx, cy - 11], [cx - 13, cy]],
                         closed=True, fc=SAPPHIRE, ec="white", lw=2, zorder=3))
    ax.text(cx, cy, "if", color="white", fontsize=26, fontweight="bold", ha="center", va="center", zorder=5)
    ax.plot([cx + 13, cx + 22], [cy, cy], color="white", lw=2, zorder=2)
    ax.text(cx + 17.5, cy + 2.3, "True", color="#B8C7D9", fontsize=11, ha="center", zorder=5)
    ax.add_patch(FancyBboxPatch((cx + 22, cy - 3.6), 22, 7.2, boxstyle="round,pad=0,rounding_size=1",
                                fc="#17A57F", ec="white", lw=1.5, zorder=3))
    ax.text(cx + 33, cy, "award", color="white", fontsize=14, fontweight="bold", ha="center", va="center",
            zorder=5)
    ax.plot([cx, cx], [cy - 11, cy - 15], color="white", lw=2, zorder=2)
    ax.text(cx + 1.5, cy - 13, "False", color="#B8C7D9", fontsize=11, ha="left", zorder=5)
    # loop arrow (counter-clockwise arc with arrowhead at its end)
    lx, ly, rr = cx, 8.6, 4.6
    t = np.linspace(0.3 * np.pi, 1.82 * np.pi, 90)
    ax.plot(lx + rr * np.cos(t), ly + rr * np.sin(t), color="#F2B84B", lw=4, solid_capstyle="round", zorder=4)
    a0, a1 = 1.74 * np.pi, 1.84 * np.pi
    ax.annotate("", xy=(lx + rr * np.cos(a1), ly + rr * np.sin(a1)),
                xytext=(lx + rr * np.cos(a0), ly + rr * np.sin(a0)),
                arrowprops=dict(arrowstyle="-|>", color="#F2B84B", lw=4, mutation_scale=22), zorder=4)
    ax.text(lx + 8, ly, "for i in range(...)", color="#F2B84B", fontsize=13, va="center",
            family="DejaVu Sans Mono", zorder=5)
    save(fig, "banner.png", dpi=130)


# =============================================================================
# Flowchart helpers
# =============================================================================
def box(ax, x, y, w, h, text, fc="white", ec=INK, tc=INK, fs=10, bold=False, r=1.2):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=1.6, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc, zorder=4,
            fontweight="bold" if bold else "normal", linespacing=1.3)


def term(ax, x, y, text, col):
    box(ax, x, y, 14, 4.2, text, fc=col, ec=col, tc="white", fs=11, bold=True, r=2.1)


def diamond(ax, x, y, w, h, text, fc="#FFF6DD", ec=WARN, fs=9.5):
    ax.add_patch(Polygon([[x, y + h / 2], [x + w / 2, y], [x, y - h / 2], [x - w / 2, y]],
                         closed=True, fc=fc, ec=ec, lw=1.8, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK, zorder=4, linespacing=1.25)


def line(ax, pts, col=INK, ls="-"):
    """Plain polyline (no arrowhead)."""
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=col, lw=1.6, zorder=2, ls=ls, solid_capstyle="butt")


def arrow(ax, pts, label=None, lpos=None, col=INK, ls="-", bg=PAPER):
    """Polyline with an arrowhead on the last segment and an optional label."""
    line(ax, pts[:-1], col, ls)
    ax.annotate("", xy=pts[-1], xytext=pts[-2],
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.6, mutation_scale=14, ls="-",
                                shrinkA=0, shrinkB=0), zorder=2)
    if label:
        ax.text(lpos[0], lpos[1], label, fontsize=9.5, color=col, fontweight="bold", ha="center",
                va="center", bbox=dict(fc=bg, ec="none", pad=1.2), zorder=5)


def canvas(w, h, title, accent):
    fig = plt.figure(figsize=(w, h), facecolor=PAPER)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100 * h / w)
    ax.axis("off")
    ax.text(3, 100 * h / w - 3, title, fontsize=17, fontweight="bold", color=INK, va="center")
    ax.add_patch(Rectangle((3, 100 * h / w - 6.3), 12, 0.7, fc=accent, ec="none"))
    return fig, ax


# =============================================================================
# 2. Flowchart: scholarship
# =============================================================================
def flow_scholarship():
    W, Hh = 10, 11.0
    H = 100 * Hh / W            # 110
    fig, ax = canvas(W, Hh, "Task 1 - Scholarship Eligibility: program flow", SAPPHIRE)
    cx = 50
    term(ax, cx, 99, "START", SAPPHIRE)
    box(ax, cx, 90, 56, 7.5, "Read name, marks, attendance, income\nre-prompt until numeric, finite and in range", fs=10)
    arrow(ax, [(cx, 96.9), (cx, 93.75)])
    # three independent checks
    xs = [20, 50, 80]
    for x, t in zip(xs, ["if marks < 80\nadd reason", "if attendance < 85\nadd reason", "if income > 50,000\nadd reason"]):
        box(ax, x, 76, 25, 7, t, fc="#EAF0FC", ec=SAPPHIRE, fs=9.5)
    line(ax, [(cx, 86.25), (cx, 83.5)])
    line(ax, [(xs[0], 83.5), (xs[2], 83.5)])
    for x in xs:
        arrow(ax, [(x, 83.5), (x, 79.5)])
    ax.text(cx + 3, 84.6, "three independent if-statements: every failure is recorded", fontsize=8.8,
            color=MUTED, ha="left", va="center", style="italic")
    line(ax, [(xs[0], 72.5), (xs[0], 69.5), (xs[2], 69.5)])
    line(ax, [(xs[2], 72.5), (xs[2], 69.5)])
    line(ax, [(cx, 72.5), (cx, 69.5)])
    diamond(ax, cx, 63.5, 34, 11, "reasons list\nnot empty?")
    ax.annotate("", xy=(cx, 69.0), xytext=(cx, 69.5),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6, mutation_scale=14), zorder=2)
    # Yes -> NOT ELIGIBLE
    box(ax, 19, 49, 24, 8.5, "NOT ELIGIBLE\nprint every reason", fc="#FDECEC", ec=BAD, fs=10)
    arrow(ax, [(cx - 17, 63.5), (19, 63.5), (19, 53.25)], "Yes", (30, 65.7), col=BAD)
    # No -> marks >= 90 ?
    diamond(ax, 74, 51, 30, 10, "marks >= 90 ?")
    arrow(ax, [(cx, 58.0), (cx, 51), (59, 51)], "No", (cx + 3.2, 55.0), col=OK)
    box(ax, 62, 36, 22, 7, "Full\nScholarship", fc="#E3F6EE", ec=OK, fs=10, bold=True)
    box(ax, 87, 36, 22, 7, "Partial\nScholarship", fc="#E3F6EE", ec=OK, fs=10, bold=True)
    line(ax, [(74, 46), (74, 42.5)], OK)
    arrow(ax, [(74, 42.5), (62, 42.5), (62, 39.5)], "Yes", (67, 42.5), col=OK)
    arrow(ax, [(74, 42.5), (87, 42.5), (87, 39.5)], "No", (81, 42.5), col=OK)
    # report
    box(ax, cx, 24, 40, 7, "Print evaluation report", fs=10.5)
    arrow(ax, [(19, 44.75), (19, 24), (30, 24)])
    arrow(ax, [(62, 32.5), (62, 27.5)])
    arrow(ax, [(87, 32.5), (87, 24), (70, 24)])
    diamond(ax, cx, 10, 34, 11, "Evaluate another\nstudent? (y/n)")
    arrow(ax, [(cx, 20.5), (cx, 15.5)])
    term(ax, 86, 10, "END", INK)
    arrow(ax, [(cx + 17, 10), (79, 10)], "n", (cx + 21.5, 12.2))
    arrow(ax, [(cx - 17, 10), (3, 10), (3, 90), (22, 90)], "y", (9, 12.2), col=SAPPHIRE, ls="--")
    save(fig, "flowchart_scholarship.png")


# =============================================================================
# 3. Flowchart: pharmacy
# =============================================================================
def flow_pharmacy():
    W, Hh = 10, 13.6
    fig, ax = canvas(W, Hh, "Task 2 - Pharmacy Inventory: program flow", JADE)
    cx = 45
    term(ax, cx, 124, "START", JADE)
    box(ax, cx, 115, 50, 6.5, "Read N = number of medicines (N >= 1)", fs=10)
    box(ax, cx, 105, 60, 7.5, "total_revenue = 0   sold_count = 0\nfailed_count = 0   restock_count = 0   restock_list = []",
        fc="#E6F6F1", ec=JADE, fs=9.5)
    arrow(ax, [(cx, 121.9), (cx, 118.25)])
    arrow(ax, [(cx, 111.75), (cx, 108.75)])
    # loop container
    ax.add_patch(FancyBboxPatch((6, 24), 88, 72, boxstyle="round,pad=0,rounding_size=2",
                                fc="white", ec=JADE, lw=2, ls="--", zorder=1))
    ax.text(9, 93.3, "for i in range(1, N + 1)", fontsize=11, fontweight="bold", color=JADE,
            family="DejaVu Sans Mono", va="center", zorder=4)
    arrow(ax, [(cx, 101.25), (cx, 89.75)])
    box(ax, cx, 86, 56, 7.5, "Read name, stock, price, quantity sold\n(each validated, re-prompts until valid)", fs=10)
    diamond(ax, cx, 73, 30, 11, "quantity > stock ?")
    arrow(ax, [(cx, 82.25), (cx, 78.5)])
    box(ax, 22, 59, 32, 9, "Reject sale\nfailed_count += 1\nremaining = stock", fc="#FDECEC", ec=BAD, fs=9.5)
    box(ax, 68, 59, 36, 10.5,
        "amount = quantity x price\ntotal_revenue += amount\nsold_count += 1\nremaining = stock - quantity",
        fc="#E3F6EE", ec=OK, fs=9.5)
    arrow(ax, [(cx - 15, 73), (22, 73), (22, 63.5)], "Yes", (27, 75.2), col=BAD, bg="white")
    arrow(ax, [(cx + 15, 73), (68, 73), (68, 64.25)], "No", (63, 75.2), col=OK, bg="white")
    # merge
    line(ax, [(22, 54.5), (22, 52), (68, 52)])
    line(ax, [(68, 53.75), (68, 52)])
    diamond(ax, cx, 44, 34, 11, f"remaining < {K['LOW_STOCK']} ?")
    arrow(ax, [(cx, 52), (cx, 49.5)])
    box(ax, 22, 32, 32, 9, "WARNING printed\nrestock_count += 1\nrestock_list.append(name)",
        fc="#FFF6DD", ec=WARN, fs=9.5)
    arrow(ax, [(cx - 17, 44), (22, 44), (22, 36.5)], "Yes", (26, 46.2), col=WARN, bg="white")
    # No branch and loop-back share the dashed rail at x = 88
    line(ax, [(cx + 17, 44), (88, 44)], OK)
    ax.text(cx + 24, 46.2, "No", fontsize=9.5, color=OK, fontweight="bold", ha="center", va="center",
            bbox=dict(fc="white", ec="none", pad=1.2), zorder=5)
    line(ax, [(38, 32), (88, 32), (88, 44)], JADE, "--")
    arrow(ax, [(88, 44), (88, 86), (73, 86)], "next i", (88, 66), col=JADE, ls="--", bg="white")
    # exit
    box(ax, cx, 15, 54, 7.5, "After the loop: print daily report\nrevenue, counters, restock list", fs=10)
    arrow(ax, [(cx, 24), (cx, 18.75)], "after the last medicine", (cx + 15, 21.4), col=MUTED)
    term(ax, cx, 5, "END", INK)
    arrow(ax, [(cx, 11.25), (cx, 7.1)])
    save(fig, "flowchart_pharmacy.png")


# =============================================================================
# 4. Scholarship decision map (marks vs attendance)
# =============================================================================
def decision_map():
    fig, ax = plt.subplots(figsize=(9, 6.4), facecolor=PAPER)
    ax.set_facecolor("white")
    ax.add_patch(Rectangle((K["MIN_MARKS"], K["MIN_ATT"]), K["FULL"] - K["MIN_MARKS"], 100 - K["MIN_ATT"],
                           fc="#FFF1CC", ec="none", zorder=0))
    ax.add_patch(Rectangle((K["FULL"], K["MIN_ATT"]), 100 - K["FULL"], 100 - K["MIN_ATT"],
                           fc="#CDEFE0", ec="none", zorder=0))
    ax.add_patch(Rectangle((50, 50), 50, 50, fc="#FBE3E3", ec="none", zorder=-1))
    ax.axvline(K["MIN_MARKS"], color=MUTED, lw=1.2, ls="--")
    ax.axvline(K["FULL"], color=MUTED, lw=1.2, ls="--")
    ax.axhline(K["MIN_ATT"], color=MUTED, lw=1.2, ls="--")
    ax.text(85, 98.2, "Partial", ha="center", fontsize=11, color="#8A6200", fontweight="bold")
    ax.text(95, 98.2, "Full", ha="center", fontsize=11, color="#127A52", fontweight="bold")
    ax.text(65, 98.2, "Not eligible on marks", ha="center", fontsize=10, color=BAD)
    ax.text(54, K["MIN_ATT"] - 1.6, "attendance below 85", fontsize=9.5, color=BAD, va="top")
    for s in R["scholarship"]:
        col = OK if s["eligible"] and s["award"].startswith("Full") else (
            WARN if s["eligible"] else BAD)
        ax.scatter(s["marks"], s["attendance"], s=130, color=col, ec=INK, lw=1.2, zorder=4,
                   marker="o" if s["income_ok"] else "X")
    # explicit label positions (x, y, horizontal alignment) so no label touches another point
    where = {"S1": (95, 92.4, "center"), "S2": (85, 90.4, "center"), "S3": (70, 77.4, "center"),
             "S4": (90, 87.6, "center"), "S5": (80, 82.4, "center"), "S6": (92, 81.4, "center"),
             "S7": (86.7, 95, "right"), "S8": (77.7, 90, "right")}
    for s_ in R["scholarship"]:
        k = s_["label"].split()[0]
        x, y, ha = where[k]
        ax.text(x, y, k, fontsize=10, fontweight="bold", color=INK, ha=ha, va="center", zorder=5)
    ax.text(50.8, 51.2, "Shaded zones assume income <= Rs. 50,000; X markers fail the income rule.",
            fontsize=8.8, color=MUTED, style="italic")
    ax.set_xlim(50, 100)
    ax.set_ylim(50, 100)
    ax.set_xlabel("Academic marks (%)", color=INK, fontsize=11)
    ax.set_ylabel("Attendance (%)", color=INK, fontsize=11)
    ax.set_title("Scholarship decision map for the 8 test scenarios", loc="left", fontsize=14,
                 fontweight="bold", color=INK, pad=12)
    from matplotlib.lines import Line2D
    ax.legend(handles=[
        Line2D([], [], marker="o", ls="", mfc=OK, mec=INK, ms=9, label="Full scholarship"),
        Line2D([], [], marker="o", ls="", mfc=WARN, mec=INK, ms=9, label="Partial scholarship"),
        Line2D([], [], marker="o", ls="", mfc=BAD, mec=INK, ms=9, label="Not eligible (income ok)"),
        Line2D([], [], marker="X", ls="", mfc=BAD, mec=INK, ms=10, label="Income above Rs. 50,000"),
    ], loc="lower right", fontsize=9, frameon=True, facecolor="white", edgecolor=LINE)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(colors=MUTED)
    save(fig, "chart_decision_map.png")


# =============================================================================
# 5. Scholarship criteria matrix
# =============================================================================
def criteria_matrix():
    rows = R["scholarship"]
    fig, ax = plt.subplots(figsize=(11, 5.4), facecolor=PAPER)
    ax.axis("off")
    cols = ["Scenario", "Marks", "Attend.", "Income (Rs.)", "Marks\n>= 80", "Attend.\n>= 85", "Income\n<= 50,000",
            "Result"]
    xs = [0.0, 3.6, 4.6, 5.8, 7.1, 8.1, 9.1, 10.7]
    ax.set_xlim(-0.2, 12.9)
    ax.set_ylim(-0.4, len(rows) + 1.2)
    for x, c in zip(xs, cols):
        ax.text(x, len(rows) + 0.55, c, fontsize=10, fontweight="bold", color=INK, va="center",
                ha="left" if x in (0.0, 10.7) else "center")
    ax.plot([-0.2, 12.9], [len(rows) + 0.05] * 2, color=INK, lw=1.4)
    for i, s in enumerate(rows):
        y = len(rows) - 1 - i + 0.35
        if i % 2 == 0:
            ax.add_patch(Rectangle((-0.2, y - 0.45), 13.1, 0.9, fc="white", ec="none", zorder=0))
        ax.text(0.0, y, s["label"], fontsize=10, color=INK, va="center")
        ax.text(xs[1], y, f"{s['marks']}", fontsize=10, color=INK, ha="center", va="center")
        ax.text(xs[2], y, f"{s['attendance']}", fontsize=10, color=INK, ha="center", va="center")
        ax.text(xs[3], y, f"{s['income']:,}", fontsize=10, color=INK, ha="center", va="center")
        for x, ok in zip(xs[4:7], (s["marks_ok"], s["attendance_ok"], s["income_ok"])):
            ax.add_patch(FancyBboxPatch((x - 0.38, y - 0.27), 0.76, 0.54, boxstyle="round,pad=0,rounding_size=0.12",
                                        fc="#CDEFE0" if ok else "#F8D3D3", ec="none"))
            ax.text(x, y, "pass" if ok else "fail", fontsize=9, ha="center", va="center",
                    color="#127A52" if ok else "#A22B2B", fontweight="bold")
        col = {"Full Scholarship": OK, "Partial Scholarship": "#B07A00"}.get(s["award"], BAD)
        ax.text(xs[7], y, s["award"] if s["eligible"] else "Not eligible", fontsize=10, fontweight="bold",
                color=col, va="center")
    ax.set_title("Criteria checks and outcome for every scenario", loc="left", fontsize=14, fontweight="bold",
                 color=INK, pad=6)
    save(fig, "chart_criteria_matrix.png")


# =============================================================================
# 6. Pharmacy results
# =============================================================================
def pharmacy_chart():
    P = R["pharmacy"]
    names = [m["name"] for m in P["medicines"]]
    stock = [m["stock"] for m in P["medicines"]]
    remaining = [m["remaining"] for m in P["medicines"]]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5), facecolor=PAPER, gridspec_kw={"width_ratios": [1.5, 1]})
    import numpy as np
    x = np.arange(len(names))
    w = 0.36
    b1 = a1.bar(x - w / 2, stock, w, color="#9FB2C8", label="Stock before")
    b2 = a1.bar(x + w / 2, remaining, w, color=[JADE if r >= P["low_stock_limit"] else WARN for r in remaining],
                label="Remaining after sale")
    a1.axhline(P["low_stock_limit"], color=BAD, lw=1.5, ls="--")
    for rect, v in list(zip(b1, stock)) + list(zip(b2, remaining)):
        a1.text(rect.get_x() + rect.get_width() / 2, v + 2.2, str(v), ha="center", fontsize=10, color=INK,
                bbox=dict(fc="white", ec="none", pad=0.8), zorder=6)
    for i, m in enumerate(P["medicines"]):
        if not m["accepted"]:
            a1.text(i, max(stock[i], 12) + 12, f"sale rejected\n({m['quantity']} > {m['stock']})", ha="center", fontsize=9.5, color=BAD,
                    fontweight="bold")
    a1.set_xticks(x)
    a1.set_xticklabels(names, color=INK)
    a1.set_title("Stock before and after each sale", loc="left", fontsize=13, fontweight="bold", color=INK)
    a1.set_ylabel("Units", color=INK)
    from matplotlib.patches import Patch
    a1.legend(handles=[Patch(color="#9FB2C8", label="Stock before"), Patch(color=JADE, label="Remaining (ok)"),
                       Patch(color=WARN, label="Remaining (below 10)"),
                       plt.Line2D([], [], color=BAD, ls="--", lw=1.5, label="Low-stock limit (10)")],
                fontsize=9, frameon=False)
    rev = [m["amount"] for m in P["medicines"]]
    bars = a2.bar(names, rev, color=[JADE if r > 0 else "#D9E0E8" for r in rev], width=0.55)
    for rect, v in zip(bars, rev):
        a2.text(rect.get_x() + rect.get_width() / 2, v + 12, f"Rs. {v:,.0f}", ha="center", fontsize=10, color=INK)
    a2.set_ylim(0, 620)
    a2.set_title(f"Revenue per medicine (total Rs. {P['total_revenue']:,.0f})", loc="left", fontsize=13,
                 fontweight="bold", color=INK)
    a2.set_ylabel("Rupees", color=INK)
    for a in (a1, a2):
        a.set_facecolor("white")
        for sp in ("top", "right"):
            a.spines[sp].set_visible(False)
        a.tick_params(colors=MUTED)
    fig.tight_layout(w_pad=3)
    save(fig, "chart_pharmacy.png")


# =============================================================================
# 7. Test results
# =============================================================================
def test_chart():
    T = R["tests"]["by_class"]
    pretty = {"TestEvaluate": "Decision logic & boundaries", "TestValidation": "Input validation",
              "TestEndToEnd": "End-to-end sessions", "TestProcessSale": "Sale calculation & stock"}
    items = []
    for k, v in T.items():
        mod, cls = k.split(".")
        prog = "Scholarship" if "scholarship" in mod else "Pharmacy"
        items.append((f"{prog}: {pretty[cls]}", v["total"], v["passed"], SAPPHIRE if prog == "Scholarship" else JADE))
    items.sort(key=lambda t: (t[3] != SAPPHIRE, -t[1]))
    fig, ax = plt.subplots(figsize=(10, 4.2), facecolor=PAPER)
    ax.set_facecolor("white")
    ys = list(range(len(items)))[::-1]
    for y, (lab, tot, passed, col) in zip(ys, items):
        ax.barh(y, tot, color="#E3E9F0", height=0.6)
        ax.barh(y, passed, color=col, height=0.6)
        ax.text(tot + 0.2, y, f"{passed}/{tot} passed", va="center", fontsize=10, color=INK)
    ax.set_yticks(ys)
    ax.set_yticklabels([i[0] for i in items], color=INK, fontsize=10)
    ax.set_xlim(0, max(i[1] for i in items) + 3)
    ax.set_xlabel("Number of tests", color=INK)
    ax.set_title(f"Automated tests: {R['tests']['total'] - R['tests']['failed']} of {R['tests']['total']} passed",
                 loc="left", fontsize=14, fontweight="bold", color=INK, pad=10)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(colors=MUTED)
    save(fig, "chart_tests.png")


# =============================================================================
# 8. Architecture diagram
# =============================================================================
def architecture():
    fig = plt.figure(figsize=(12, 6.4), facecolor=PAPER)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 53)
    ax.axis("off")
    ax.text(3, 50, "Code structure: functions in each program", fontsize=17, fontweight="bold", color=INK, va="center")

    def panel(x0, title, col, fns, consts):
        ax.add_patch(FancyBboxPatch((x0, 1.5), 45, 43.5, boxstyle="round,pad=0,rounding_size=1.5", fc="white", ec=col, lw=2))
        ax.add_patch(FancyBboxPatch((x0, 39.5), 45, 5.5, boxstyle="round,pad=0,rounding_size=1.5", fc=col, ec=col))
        ax.text(x0 + 22.5, 42.2, title, color="white", fontsize=12.5, fontweight="bold", ha="center", va="center")
        ax.text(x0 + 2.5, 36.6, consts, fontsize=9, color=MUTED, va="center", family="DejaVu Sans Mono")
        y = 31
        for name, desc, main in fns:
            fc = "#EAF0FC" if col == SAPPHIRE else "#E6F6F1"
            if main:
                fc = col
            box(ax, x0 + 22.5, y, 40, 4.4, "", fc=fc, ec=col, r=0.9)
            ax.text(x0 + 4, y + 0.55, name, fontsize=10, fontweight="bold", color="white" if main else INK,
                    va="center", family="DejaVu Sans Mono")
            ax.text(x0 + 4, y - 1.35, desc, fontsize=8.4, color="#E6EEF8" if main else MUTED, va="center")
            y -= 5.0

    panel(3, "student_scholarship_system.py", SAPPHIRE, [
        ("is_valid_name(name)", "letters, spaces, - ' . only", False),
        ("get_name()", "prompt loop for the name", False),
        ("get_number(prompt, min, max)", "numeric, finite, in range", False),
        ("evaluate(marks, att, income)", "if / elif / else -> award, reasons", False),
        ("print_report(...)", "formatted evaluation report", False),
        ("main()", "while True: ask, evaluate, report, repeat", True),
    ], "MIN_MARKS=80  FULL=90  ATT=85  INC=50000")
    panel(52, "pharmacy_inventory_system.py", JADE, [
        ("get_int(prompt, minimum)", "whole number >= minimum", False),
        ("get_price(prompt)", "finite number > 0", False),
        ("get_medicine_name()", "non-empty name", False),
        ("process_sale(stock, price, qty)", "accept/reject, amount, remaining", False),
        ("main()", "for i in range(1, N + 1): ...", True),
    ], "LOW_STOCK_LIMIT = 10")
    save(fig, "architecture.png")


if __name__ == "__main__":
    banner()
    flow_scholarship()
    flow_pharmacy()
    decision_map()
    criteria_matrix()
    pharmacy_chart()
    test_chart()
    architecture()
