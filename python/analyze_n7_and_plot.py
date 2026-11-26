#!/usr/bin/env python3
"""
Full n <= 7 Exhaustive Analysis (all 994 non-isomorphic connected graphs:
2 + 6 + 21 + 112 + 853) + Publication-Quality Figure Generation.
"""
import os
from pathlib import Path
import networkx as nx
ROOT = Path(__file__).resolve().parents[1]
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from itertools import combinations
from math import comb, sqrt

def dist_matrix(adj: np.ndarray) -> np.ndarray:
    n = adj.shape[0]
    D = np.where(adj > 0, 1, 10**9)
    np.fill_diagonal(D, 0)
    for k in range(n):
        D = np.minimum(D, D[:, k:k + 1] + D[k:k + 1, :])
    return D

def is_path(adj: np.ndarray, D: np.ndarray) -> bool:
    n = adj.shape[0]
    degs = sorted(np.sum(adj, axis=1).tolist())
    return int(np.max(D)) < 10**8 and degs == ([1, 1] + [2] * (n - 2))

def analyze_graph(adj: np.ndarray):
    n = adj.shape[0]
    D = dist_matrix(adj)
    W = int(np.sum(D) // 2)
    diam = int(np.max(D))
    tr = np.sum(D, axis=1)
    eL = np.linalg.eigvalsh(np.diag(tr) - D)[::-1]
    eQ = np.linalg.eigvalsh(np.diag(tr) + D)[::-1]
    path_flag = is_path(adj, D)

    vL, rL = max((float(np.sum(eL[:r])) - (W + comb(r + 2, 3)), r) for r in range(1, n + 1))
    vQ, rQ = max((float(np.sum(eQ[:r])) - (W + comb(r + 2, 3)), r) for r in range(1, n + 1))
    vLc = max(float(np.sum(eL[:r])) - (W + diam * comb(r + 1, 2)) for r in range(1, n + 1))
    vQc = max(float(np.sum(eQ[:r])) - (W + diam * comb(r + 1, 2)) for r in range(1, n + 1))
    return {
        "n": n, "m": int(np.sum(adj) // 2), "W": W, "diam": diam, "is_path": path_flag,
        "vL": vL, "rL": rL, "vQ": vQ, "rQ": rQ, "vLc": vLc, "vQc": vQc,
    }

# Collect exhaustive n=3,4,5,6 + n=7 from C++ masks
summary = {}
by_diam_n7 = {}

for n in [3, 4, 5, 6]:
    edges_all = list(combinations(range(n), 2))
    m_all = len(edges_all)
    seen = {}
    records = []
    for mask in range(1 << m_all):
        if bin(mask).count("1") < n - 1:
            continue
        adj = np.zeros((n, n), int)
        for idx in range(m_all):
            if (mask >> idx) & 1:
                u, v = edges_all[idx]
                adj[u, v] = adj[v, u] = 1
        D = dist_matrix(adj)
        if int(np.max(D)) >= 10**8:
            continue
        tr = np.sum(D, axis=1)
        eL = np.linalg.eigvalsh(np.diag(tr) - D)[::-1]
        eQ = np.linalg.eigvalsh(np.diag(tr) + D)[::-1]
        sig = (tuple(sorted(np.sum(adj, axis=1).tolist())), tuple(sorted(tr.tolist())),
               tuple(np.round(eL, 5).tolist()), tuple(np.round(eQ, 5).tolist()))
        graph = nx.from_numpy_array(adj)
        bucket = seen.setdefault(sig, [])
        if any(nx.is_isomorphic(graph, old) for old in bucket):
            continue
        bucket.append(graph)
        records.append(analyze_graph(adj))
    assert len(records) == {3: 2, 4: 6, 5: 21, 6: 112}[n]
    summary[n] = records

# Now n=7 from n7_masks.txt
edges_7 = list(combinations(range(7), 2))
records_7 = []
with open(ROOT / "n7_masks.txt") as f:
    for line in f:
        mask = int(line.strip())
        adj = np.zeros((7, 7), int)
        for idx in range(21):
            if (mask >> idx) & 1:
                u, v = edges_7[idx]
                adj[u, v] = adj[v, u] = 1
        rec = analyze_graph(adj)
        records_7.append(rec)
assert len(records_7) == 853
summary[7] = records_7

print("=== COMPLETE EXHAUSTIVE STATISTICS n = 3..7 (994 GRAPHS) ===")
stats_out = {}
for n in [3, 4, 5, 6, 7]:
    recs = summary[n]
    tot = len(recs)
    dl_v = [r for r in recs if r["vL"] > 1e-7]
    dq_np_v = [r for r in recs if r["vQ"] > 1e-7 and not r["is_path"]]
    dq_all_v = [r for r in recs if r["vQ"] > 1e-7]
    corr_dl = sum(1 for r in recs if r["vLc"] > 1e-7)
    corr_dq = sum(1 for r in recs if r["vQc"] > 1e-7)
    max_dl = max((r["vL"] for r in recs), default=0.0)
    max_dq_np = max((r["vQ"] for r in recs if not r["is_path"]), default=0.0)
    assert corr_dl == 0 and corr_dq == 0
    stats_out[n] = {
        "total": tot, "dl_viol": len(dl_v), "dq_nonpath_viol": len(dq_np_v),
        "dq_all_viol": len(dq_all_v), "max_dl": max_dl, "max_dq_nonpath": max_dq_np,
    }
    print(f"n={n}: total={tot:3d} | DL viol={len(dl_v):3d} ({100*len(dl_v)/tot:5.1f}%) max={max_dl:+7.3f} | "
          f"DQ(non-path) viol={len(dq_np_v):3d} ({100*len(dq_np_v)/(tot-1 if n>=4 else tot):5.1f}%) max={max_dq_np:+7.3f} | "
          f"Corrected viol=0/0")

# Breakdown of n=7 by diameter
print("\n=== n=7 BREAKDOWN BY DIAMETER ===")
for d in sorted(set(r["diam"] for r in records_7)):
    sub = [r for r in records_7 if r["diam"] == d]
    dl_c = sum(1 for r in sub if r["vL"] > 1e-7)
    dq_c = sum(1 for r in sub if r["vQ"] > 1e-7 and not r["is_path"])
    by_diam_n7[d] = (len(sub), dl_c, dq_c)
    print(f"  diam={d}: total={len(sub):3d} | DL viol={dl_c:3d} | DQ(non-path) viol={dq_c:3d}")

# ============================================================
# GENERATE 3 PUBLICATION-QUALITY FIGURES (PDF + 300-DPI PNG)
# ============================================================
fig_dir = str(ROOT / "paper" / "figures")
os.makedirs(fig_dir, exist_ok=True)
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "legend.fontsize": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# --- FIGURE 1: Exhaustive n=3..7 violation counts & n=7 diameter breakdown ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.0))
ns = [3, 4, 5, 6, 7]
x = np.arange(len(ns))
w = 0.27
dl_pcts = [100 * stats_out[n]["dl_viol"] / stats_out[n]["total"] for n in ns]
dq_pcts = [100 * stats_out[n]["dq_nonpath_viol"] / max(1, stats_out[n]["total"] - 1) for n in ns]
corr_pcts = [0.0 for _ in ns]

b1 = ax1.bar(x - w, dl_pcts, width=w, color="#1f4e79", label=r"Zhou et al. ($D^L$)")
b2 = ax1.bar(x, dq_pcts, width=w, color="#c0392b", label=r"Alhevaz et al. ($D^Q$, non-path)")
b3 = ax1.bar(x + w, corr_pcts, width=w, color="#27ae60", label=r"Corrected Bound (Thm. 5.1)")
for bar, n_val in zip(b1, ns):
    c = stats_out[n_val]["dl_viol"]
    if c > 0:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8, f"{c}", ha="center", va="bottom", fontsize=8)
for bar, n_val in zip(b2, ns):
    c = stats_out[n_val]["dq_nonpath_viol"]
    if c > 0:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8, f"{c}", ha="center", va="bottom", fontsize=8)
ax1.set_xticks(x)
ax1.set_xticklabels([f"n={n}\n({stats_out[n]['total']})" for n in ns])
ax1.set_ylabel("Violating Graphs (%)")
ax1.set_title("(a) Exhaustive Refutation Rate ($n \\leq 7$, 994 Graphs)")
ax1.set_ylim(0, 46)
ax1.legend(frameon=False, loc="upper right")
ax1.grid(axis="y", linestyle="--", alpha=0.35)

diams = sorted(by_diam_n7.keys())
xd = np.arange(len(diams))
dl_d = [100 * by_diam_n7[d][1] / by_diam_n7[d][0] for d in diams]
dq_d = [100 * by_diam_n7[d][2] / max(1, by_diam_n7[d][0] - (1 if d == 6 else 0)) for d in diams]
ax2.bar(xd - 0.18, dl_d, width=0.36, color="#1f4e79", label=r"Zhou et al. ($D^L$)")
ax2.bar(xd + 0.18, dq_d, width=0.36, color="#c0392b", label=r"Alhevaz et al. ($D^Q$, non-path)")
ax2.set_xticks(xd)
ax2.set_xticklabels([f"D={d}\n({by_diam_n7[d][0]})" for d in diams])
ax2.set_ylabel("Violating Graphs (%)")
ax2.set_title("(b) Violation Rate by Diameter at $n = 7$ (853 Graphs)")
ax2.set_ylim(0, 112)
ax2.legend(frameon=False, loc="upper left")
ax2.grid(axis="y", linestyle="--", alpha=0.35)

plt.tight_layout()
plt.savefig(f"{fig_dir}/fig1_exhaustive_n3_to_n7.pdf", bbox_inches="tight")
plt.savefig(f"{fig_dir}/fig1_exhaustive_n3_to_n7.png", dpi=300, bbox_inches="tight")
plt.close()

# --- FIGURE 2: Asymptotic Theta(n^3) Scaling up to n=120 ---
def path_graph(n):
    A = np.zeros((n, n), int)
    for i in range(n-1): A[i, i+1] = A[i+1, i] = 1
    return A

def broom_graph(n):
    A = np.zeros((n, n), int)
    for i in range(n-3): A[i, i+1] = A[i+1, i] = 1
    A[n-3, n-2] = A[n-2, n-3] = A[n-3, n-1] = A[n-1, n-3] = 1
    return A

def lollipop_graph(n):
    A = np.zeros((n, n), int)
    A[0,1]=A[1,0]=A[1,2]=A[2,1]=A[0,2]=A[2,0]=1
    for i in range(2, n-1): A[i, i+1] = A[i+1, i] = 1
    return A

n_vals = list(range(12, 121, 6))
dl_broom_opt, dq_broom_opt, schur_broom_opt = [], [], []
dl_lolli_opt, dq_lolli_opt = [], []
for n in n_vals:
    for builder, dl_arr, dq_arr, sc_arr in [
        (broom_graph, dl_broom_opt, dq_broom_opt, schur_broom_opt),
        (lollipop_graph, dl_lolli_opt, dq_lolli_opt, None),
    ]:
        A = builder(n)
        D = dist_matrix(A)
        W = int(np.sum(D) // 2)
        tr = np.sum(D, axis=1)
        eL = np.linalg.eigvalsh(np.diag(tr) - D)[::-1]
        eQ = np.linalg.eigvalsh(np.diag(tr) + D)[::-1]
        tr_s = sorted(tr.tolist(), reverse=True)
        # optimal r
        dl_arr.append(max(float(np.sum(eL[:r])) - (W + comb(r+2, 3)) for r in range(1, n+1)) / (n**3))
        dq_arr.append(max(float(np.sum(eQ[:r])) - (W + comb(r+2, 3)) for r in range(1, n+1)) / (n**3))
        if sc_arr is not None:
            sc_arr.append(max(sum(tr_s[:r]) - (W + comb(r+2, 3)) for r in range(1, n+1)) / (n**3))

fig, ax = plt.subplots(figsize=(7.2, 4.0))
ax.plot(n_vals, dl_broom_opt, "o-", color="#1f4e79", lw=2, ms=4, label=r"$B(n-2,2)$: max $D^L$ excess $/ n^3$")
ax.plot(n_vals, dq_broom_opt, "s--", color="#c0392b", lw=2, ms=4, label=r"$B(n-2,2)$: max $D^Q$ excess $/ n^3$")
ax.plot(n_vals, schur_broom_opt, "^:", color="#8e44ad", lw=1.8, ms=4, label=r"$B(n-2,2)$: Schur diagonal excess $/ n^3$")
ax.axhline(sqrt(3)/2 - 5/6, color="#27ae60", ls="-.", lw=1.5, label=r"Analytical Schur limit $\frac{\sqrt{3}}{2}-\frac{5}{6} \approx 0.03269$")
ax.axhline(5/162, color="#7f8c8d", ls=":", lw=1.3, label=r"Lean-verified $r=2\lfloor n/3\rfloor$ limit $\frac{5}{162} \approx 0.03086$")
ax.set_xlabel("Order $n$")
ax.set_ylabel(r"Normalized Violation $\mathrm{Excess} / n^3$")
ax.set_title(r"Catastrophic $\Theta(n^3)$ Violation on Non-Path Broom Trees $B(n-2,2)$")
ax.set_ylim(0.015, 0.042)
ax.legend(frameon=False, loc="lower right")
ax.grid(True, linestyle="--", alpha=0.35)
plt.tight_layout()
plt.savefig(f"{fig_dir}/fig2_asymptotic_cubic.pdf", bbox_inches="tight")
plt.savefig(f"{fig_dir}/fig2_asymptotic_cubic.png", dpi=300, bbox_inches="tight")
plt.close()

# --- FIGURE 3: Profile across r=1..30 for Broom B(28, 2) (n=30) ---
n = 30
A = broom_graph(n)
D = dist_matrix(A)
W = int(np.sum(D) // 2)
diam = int(np.max(D))
tr = np.sum(D, axis=1)
tr_s = sorted(tr.tolist(), reverse=True)
eL = np.linalg.eigvalsh(np.diag(tr) - D)[::-1]
eQ = np.linalg.eigvalsh(np.diag(tr) + D)[::-1]
rs = np.arange(1, n + 1)
uL = [float(np.sum(eL[:r])) for r in rs]
uQ = [float(np.sum(eQ[:r])) for r in rs]
diag_sum = [sum(tr_s[:r]) for r in rs]
conj_rhs = [W + comb(int(r)+2, 3) for r in rs]
corr_rhs = [W + diam * comb(int(r)+1, 2) for r in rs]

fig, ax = plt.subplots(figsize=(7.2, 4.0))
ax.plot(rs, corr_rhs, "-", color="#27ae60", lw=2.2, label=r"Corrected Bound $W + D\binom{r+1}{2}$ (Thm. 5.1)")
ax.plot(rs, uL, "-", color="#1f4e79", lw=2.0, label=r"Distance Laplacian $U_r(B(28,2))$")
ax.plot(rs, uQ, "--", color="#c0392b", lw=1.8, label=r"Distance Signless Laplacian $M_r^Q(B(28,2))$")
ax.plot(rs, diag_sum, ":", color="#8e44ad", lw=1.6, label=r"Schur Diagonal Lower Bound $\sum_{v\in S}\mathrm{Tr}(v)$")
ax.plot(rs, conj_rhs, "-.", color="#e67e22", lw=2.0, label=r"Refuted Conjectured Bound $W + \binom{r+2}{3}$")
ax.fill_between(rs, conj_rhs, uL, where=[a > b for a, b in zip(uL, conj_rhs)], color="#e74c3c", alpha=0.18, label="Violation Region")
ax.set_xlabel("Number of Eigenvalues $r$")
ax.set_ylabel("Spectral Sum / Bound Value")
ax.set_title(r"Spectral Sums vs. Refuted and Corrected Bounds on Non-Path Tree $B(28,2)$ ($n=30, D=28$)")
ax.legend(frameon=False, loc="upper left", fontsize=8.5)
ax.grid(True, linestyle="--", alpha=0.35)
plt.tight_layout()
plt.savefig(f"{fig_dir}/fig3_corrected_bound_comparison.pdf", bbox_inches="tight")
plt.savefig(f"{fig_dir}/fig3_corrected_bound_comparison.png", dpi=300, bbox_inches="tight")
plt.close()

print("\nGenerated 3 publication-quality figures in", fig_dir)
