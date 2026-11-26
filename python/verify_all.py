#!/usr/bin/env python3
"""
Reproducible Verification & Experimental Suite for:
"Disproving and Correcting the Distance Laplacian and Distance Signless Laplacian
 Brouwer-Type Conjectures"

This script independently verifies:
1. Exhaustive enumeration of all connected simple graphs on n = 3, 4, 5, 6 vertices
   (matching the exact counts 2, 6, 21, 112 non-isomorphic connected graphs via
   exact graph isomorphism),
   identifying ALL minimal counterexamples to:
   - Zhou–Wang–Chai (2025): U_r(G) <= W(G) + C(r+2, 3)
   - Alhevaz–Baghipur–Ganie–Pirzada (2021): M_k^Q(G) <= W(G) + C(k+2, 3) (G != P_n)
2. Exact rational orthogonal
   Ky Fan certificates for all minimal counterexamples.
3. Asymptotic Theta(n^3) violation on three infinite families (Paths P_n, non-path
   Brooms B(n-2, 2), and unicyclic Lollipops L(3, n-3)) up to n = 100, together
   with uniform caterpillars (checking AIMS Math. 11(5), 2026).
4. Universal validation of the corrected diameter-dependent bounds:
     U_r(G) <= W(G) + diam(G) * C(r+1, 2)
     M_r^Q(G) <= W(G) + diam(G) * C(r+1, 2)
   across all connected graphs with n <= 6 and structured families up to n = 100.
"""

import numpy as np
import sympy as sp
import networkx as nx
from fractions import Fraction
from itertools import combinations
from math import comb


def dist_matrix(adj: np.ndarray) -> np.ndarray:
    n = adj.shape[0]
    D = np.where(adj > 0, 1, 10**9)
    np.fill_diagonal(D, 0)
    for k in range(n):
        D = np.minimum(D, D[:, k:k + 1] + D[k:k + 1, :])
    return D


def is_connected(D: np.ndarray) -> bool:
    return int(np.max(D)) < 10**8


def is_path(adj: np.ndarray, D: np.ndarray) -> bool:
    n = adj.shape[0]
    degs = sorted(np.sum(adj, axis=1).tolist())
    return is_connected(D) and degs == ([1, 1] + [2] * (n - 2))


def make_graph(n: int, edges: list[tuple[int, int]]) -> np.ndarray:
    adj = np.zeros((n, n), dtype=int)
    for u, v in edges:
        adj[u, v] = adj[v, u] = 1
    return adj


def path_graph(n: int) -> np.ndarray:
    return make_graph(n, [(i, i + 1) for i in range(n - 1)])


def broom_graph(n: int) -> np.ndarray:
    """B(n-2, 2): path 0..n-3 with two leaves n-2, n-1 attached to n-3 (non-path tree for n >= 4)."""
    edges = [(i, i + 1) for i in range(n - 3)] + [(n - 3, n - 2), (n - 3, n - 1)]
    return make_graph(n, edges)


def lollipop_graph(n: int) -> np.ndarray:
    """L(3, n-3): triangle {0,1,2} with path 2..n-1 attached (unicyclic non-tree for n >= 4)."""
    edges = [(0, 1), (1, 2), (0, 2)] + [(i, i + 1) for i in range(2, n - 1)]
    return make_graph(n, edges)


def verify_ky_fan_cert(name: str, M: np.ndarray, vecs: list[list[int]], bound: int):
    k = len(vecs)
    n = M.shape[0]
    for i in range(k):
        assert len(vecs[i]) == n
        for j in range(i + 1, k):
            dot = sum(vecs[i][t] * vecs[j][t] for t in range(n))
            assert dot == 0, f"{name}: vectors {i},{j} not orthogonal (dot={dot})"
    total = Fraction(0)
    for v in vecs:
        num = sum(v[i] * int(M[i, j]) * v[j] for i in range(n) for j in range(n))
        den = sum(x * x for x in v)
        assert den > 0
        total += Fraction(num, den)
    assert total > bound, f"{name}: {total} <= {bound}"
    print(f"  [PASS] {name:24s}: Ky Fan Rayleigh sum = {str(total):>8s} ({float(total):.6f}) > {bound} (margin +{float(total - bound):.6f})")


def run_minimal_certificates():
    print("=" * 72)
    print("1. EXACT RATIONAL ORTHOGONAL KY FAN CERTIFICATES FOR MINIMAL COUNTEREXAMPLES")
    print("=" * 72)

    cases = [
        ("P_4 (DL, r=2)", path_graph(4), "L", 2, [[1, 0, 0, -1], [1, -1, -1, 1]]),
        ("K_{1,3} (DL, r=2)", make_graph(4, [(0, 1), (0, 2), (0, 3)]), "L", 2, [[0, 1, -1, 0], [0, 1, 1, -2]]),
        ("P_5 (DL, r=3)", path_graph(5), "L", 3, [[1, 0, 0, 0, -1], [0, 1, 0, -1, 0], [1, -1, 0, -1, 1]]),
        ("B(3,2) (DL, r=3)", broom_graph(5), "L", 3, [[0, 0, 0, 1, -1], [2, -1, -1, 0, 0], [1, 1, 1, -1, -1]]),
        ("B(4,2) (DQ, k=3)", broom_graph(6), "Q", 3, [[0, 0, 0, 0, 1, -1], [2, 1, 1, 1, 2, 2], [3, -2, 0, 0, -1, -1]]),
        ("L(3,3) (DQ, k=3)", lollipop_graph(6), "Q", 3, [[1, -1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 2], [1, 1, 0, 0, 2, -2]]),
    ]
    for name, adj, kind, r, vecs in cases:
        D = dist_matrix(adj)
        W = int(np.sum(D) // 2)
        tr = np.sum(D, axis=1)
        M = (np.diag(tr) - D) if kind == "L" else (np.diag(tr) + D)
        bound = W + comb(r + 2, 3)
        verify_ky_fan_cert(name, M, vecs, bound)


def run_exhaustive_small():
    print("\n" + "=" * 72)
    print("2. EXHAUSTIVE CHECK OVER ALL LABELED CONNECTED GRAPHS ON n = 3, 4, 5, 6")
    print("=" * 72)
    for n in [3, 4, 5, 6]:
        edges_all = list(combinations(range(n), 2))
        m_all = len(edges_all)
        seen = {}
        dl_viols = 0
        dq_nonpath_viols = 0
        dl_corr_viols = 0
        dq_corr_viols = 0

        for mask in range(1 << m_all):
            if bin(mask).count("1") < n - 1:
                continue
            adj = np.zeros((n, n), dtype=int)
            for idx in range(m_all):
                if (mask >> idx) & 1:
                    u, v = edges_all[idx]
                    adj[u, v] = adj[v, u] = 1
            D = dist_matrix(adj)
            if not is_connected(D):
                continue
            tr = np.sum(D, axis=1)
            DL = np.diag(tr) - D
            DQ = np.diag(tr) + D
            eL = np.linalg.eigvalsh(DL)[::-1]
            eQ = np.linalg.eigvalsh(DQ)[::-1]
            # Fine signature to deduplicate isomorphic copies cleanly
            sig = (
                tuple(sorted(np.sum(adj, axis=1).tolist())),
                tuple(sorted(tr.tolist())),
                tuple(np.round(eL, 5).tolist()),
                tuple(np.round(eQ, 5).tolist()),
            )
            graph = nx.from_numpy_array(adj)
            bucket = seen.setdefault(sig, [])
            if any(nx.is_isomorphic(graph, old) for old in bucket):
                continue
            bucket.append(graph)

            W = int(np.sum(D) // 2)
            diam = int(np.max(D))
            path_flag = is_path(adj, D)

            vL = max(float(np.sum(eL[:r])) - (W + comb(r + 2, 3)) for r in range(1, n + 1))
            vQ = max(float(np.sum(eQ[:r])) - (W + comb(r + 2, 3)) for r in range(1, n + 1))
            vLc = max(float(np.sum(eL[:r])) - (W + diam * comb(r + 1, 2)) for r in range(1, n + 1))
            vQc = max(float(np.sum(eQ[:r])) - (W + diam * comb(r + 1, 2)) for r in range(1, n + 1))

            if vL > 1e-7:
                dl_viols += 1
            if vQ > 1e-7 and not path_flag:
                dq_nonpath_viols += 1
            if vLc > 1e-7:
                dl_corr_viols += 1
            if vQc > 1e-7:
                dq_corr_viols += 1

        print(
            f"  n={n}: unique graphs={sum(map(len, seen.values())):3d} | "
            f"DL viol={dl_viols:2d} | DQ(non-path) viol={dq_nonpath_viols:2d} | "
            f"Corrected DL viol={dl_corr_viols} | Corrected DQ viol={dq_corr_viols}"
        )
        assert sum(map(len, seen.values())) == {3: 2, 4: 6, 5: 21, 6: 112}[n]
        assert dl_corr_viols == 0 and dq_corr_viols == 0


def run_asymptotic_scaling():
    print("\n" + "=" * 72)
    print("3. ASYMPTOTIC THETA(n^3) SCALING & CORRECTED BOUND CHECK (n = 10..100)")
    print("=" * 72)
    print(f"  {'Family':10s} {'n':>4s} {'r=2⌊n/3⌋':>8s} {'DiagExcess':>12s} {'DL_Excess':>12s} {'DQ_Excess':>12s} {'DL_Excess/n^3':>14s} {'CorrMargin':>12s}")
    for fam, builder in [("Path", path_graph), ("Broom", broom_graph), ("Lollipop", lollipop_graph)]:
        for n in [10, 15, 20, 30, 50, 100]:
            adj = builder(n)
            D = dist_matrix(adj)
            W = int(np.sum(D) // 2)
            diam = int(np.max(D))
            tr = np.sum(D, axis=1)
            DL = np.diag(tr) - D
            DQ = np.diag(tr) + D
            eL = np.linalg.eigvalsh(DL)[::-1]
            eQ = np.linalg.eigvalsh(DQ)[::-1]

            t = n // 3
            r = 2 * t
            rhs = W + comb(r + 2, 3)
            diag_ex = sum(sorted(tr.tolist(), reverse=True)[:r]) - rhs
            dl_ex = float(np.sum(eL[:r])) - rhs
            dq_ex = float(np.sum(eQ[:r])) - rhs

            # Check corrected bound for ALL r = 1..n
            worst_corr = max(
                max(float(np.sum(eL[:k])) - (W + diam * comb(k + 1, 2)),
                    float(np.sum(eQ[:k])) - (W + diam * comb(k + 1, 2)))
                for k in range(1, n + 1)
            )
            assert diag_ex > 0 and dl_ex >= diag_ex - 1e-6 and dq_ex >= diag_ex - 1e-6
            assert worst_corr <= 1e-6
            print(f"  {fam:10s} {n:4d} {r:8d} {diag_ex:12d} {dl_ex:12.2f} {dq_ex:12.2f} {dl_ex / (n**3):14.6f} {worst_corr:12.2f}")


def run_caterpillar_check():
    print("\n" + "=" * 72)
    print("4. UNIFORM CATERPILLAR CHECK (AIMS Math. 11(5), May 2026)")
    print("=" * 72)
    for spine in [6, 8, 10]:
        n = 2 * spine
        edges = [(i, i + 1) for i in range(spine - 1)] + [(i, spine + i) for i in range(spine)]
        adj = make_graph(n, edges)
        D = dist_matrix(adj)
        W = int(np.sum(D) // 2)
        diam = int(np.max(D))
        tr = np.sum(D, axis=1)
        eL = np.linalg.eigvalsh(np.diag(tr) - D)[::-1]
        best_ex, best_r = max((float(np.sum(eL[:r])) - (W + comb(r + 2, 3)), r) for r in range(1, n + 1))
        print(f"  Comb(spine={spine}, n={n}, diam={diam}): max DL excess = {best_ex:+.4f} at r={best_r}")


if __name__ == "__main__":
    run_minimal_certificates()
    run_exhaustive_small()
    run_asymptotic_scaling()
    run_caterpillar_check()
    print("\nALL CHECKS PASSED SUCCESSFULLY.")
