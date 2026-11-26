"""Independent exact-root-interval census (requires networkx, numpy, sympy).
Graph atlas coverage is inherited from NetworkX; all spectral comparisons use
rational isolating intervals, not floating-point eigenvalues.
"""
import math
from collections import Counter, defaultdict
import networkx as nx
import numpy as np
import sympy as sp

def root_intervals(A):
    poly = sp.Poly(sp.Matrix(A.tolist()).charpoly().as_expr())
    roots = [ab for ab, m in poly.intervals(eps=sp.Rational(1, 10**9))[::-1] for _ in range(m)]
    assert len(roots) == len(A)
    return roots

def matrices(g):
    # BFS distances are integers; no floating-point distance conversion needed.
    nodelist = list(g)
    dd = dict(nx.all_pairs_shortest_path_length(g))
    d = np.array([[dd[u][v] for v in nodelist] for u in nodelist], dtype=int)
    return d, np.diag(d.sum(1)), int(d.sum()//2), int(d.max())

def main():
    rows = defaultdict(Counter)
    uncertain = []
    for g in nx.graph_atlas_g():
        n = len(g)
        if n < 2 or not nx.is_connected(g):
            continue
        d, T, W, D = matrices(g)
        path = max(dict(g.degree()).values()) <= 2 and g.number_of_edges() == n-1
        rows[n]["connected"] += 1
        for label, A in [("DL", T-d), ("DQ", T+d)]:
            lo = hi = sp.S(0)
            yes = False
            unc = []
            for k, (a,b) in enumerate(root_intervals(A), 1):
                lo += a
                hi += b
                bound = W + math.comb(k+2, 3)
                if lo > bound:
                    yes = True
                elif hi > bound:
                    unc.append(k)
                corrected = W + D*math.comb(k+1, 2)
                if hi > corrected:
                    uncertain.append((n, label, k, "corrected"))
            if label == "DL" or not path:
                rows[n][label] += int(yes)
                if unc and not yes:
                    uncertain.append((n, label, unc, "original"))
    assert not uncertain, uncertain
    expected = [(1,0,0),(2,0,0),(6,2,0),(21,6,0),(112,19,6),(853,61,16)]
    assert [(rows[n]["connected"],rows[n]["DL"],rows[n]["DQ"]) for n in range(2,8)] == expected
    for n in range(2,8):
        print(n, dict(rows[n]))
    for h in (6,8):
        g = nx.path_graph(h)
        g.add_edges_from((i,h+i) for i in range(h))
        d,T,W,D = matrices(g)
        roots = root_intervals(T-d)
        low = sum(a for a,b in roots[:h+1])
        high = sum(b for a,b in roots[:h+1])
        bound = W + math.comb(h+3,3)
        assert low > bound
        print("comb",h,"W",W,"r",h+1,"rational interval",low,high,"threshold",bound)

if __name__ == "__main__":
    main()
