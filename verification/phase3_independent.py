"""Phase-3 independent verification of the distance Brouwer-type census.

Written from scratch (no code from python/verify_all.py, no networkx):
  * exact isomorphism-free generation of all connected graphs on 2..7 vertices
  * exact integer distance matrices (BFS on bitsets)
  * distance Laplacian L = diag(tr) - D and signless Q = diag(tr) + D
  * independent recomputation of the violation counts in the manuscript
  * exact rational verification of every published Ky Fan certificate
  * random search for counterexamples to the corrected bound W + D*C(r+1,2)
  * numerical check of the three Theta(n^3) families and of a proposed sharper bound

Usage: python phase3_independent.py [--quick]
"""
import sys
from itertools import permutations, product
from math import comb
from fractions import Fraction as F
import numpy as np

# ---------------------------------------------------------------- canonical form
def refine(n, rows, colors):
    while True:
        sig = [(colors[v], tuple(sorted(colors[u] for u in range(n) if rows[v] >> u & 1)))
               for v in range(n)]
        order = {s: i for i, s in enumerate(sorted(set(sig)))}
        new = [order[s] for s in sig]
        if len(set(new)) == len(set(colors)):
            return new
        colors = new

def canon(n, rows):
    """Lexicographically minimal adjacency code over all isomorphisms."""
    colors = refine(n, rows, [bin(r).count("1") for r in rows])
    cells = {}
    for v, c in enumerate(colors):
        cells.setdefault(c, []).append(v)
    blocks = [cells[c] for c in sorted(cells)]
    best = None
    for choice in product(*[list(permutations(b)) for b in blocks]):
        order = [v for blk in choice for v in blk]
        code = []
        for i in order:
            bits = 0
            for j, v in enumerate(order):
                if rows[i] >> v & 1:
                    bits |= 1 << j
            code.append(bits)
        code = tuple(code)
        if best is None or code < best:
            best = code
    return best

def connected(n, rows):
    seen, stack = 1, [0]
    while stack:
        v = stack.pop()
        nb = rows[v] & ~seen
        while nb:
            u = (nb & -nb).bit_length() - 1
            nb &= nb - 1
            seen |= 1 << u
            stack.append(u)
    return seen == (1 << n) - 1

def generate(max_n):
    """graphs[n] = list of canonical row-tuples for all connected graphs on n vertices."""
    graphs = {1: [(0,)]}
    for n in range(2, max_n + 1):
        found = {}
        for g in graphs[n - 1]:
            base = list(g) + [0]
            for mask in range(1, 1 << (n - 1)):
                rows = list(base)
                for v in range(n - 1):
                    if mask >> v & 1:
                        rows[v] |= 1 << (n - 1)
                rows[n - 1] = mask
                code = canon(n, rows)
                found[code] = code
        graphs[n] = sorted(found.values())
        print(f"  n={n}: {len(graphs[n])} connected graphs", flush=True)
    return graphs

# ---------------------------------------------------------------- linear algebra
def distances(n, rows):
    d = [[0] * n for _ in range(n)]
    for s in range(n):
        dist = [-1] * n
        dist[s] = 0
        queue = [s]
        head = 0
        while head < len(queue):
            v = queue[head]
            head += 1
            nb = rows[v]
            while nb:
                u = (nb & -nb).bit_length() - 1
                nb &= nb - 1
                if dist[u] < 0:
                    dist[u] = dist[v] + 1
                    queue.append(u)
        d[s] = dist
    return d

def matrices(n, d):
    tr = [sum(d[i]) for i in range(n)]
    W = sum(tr) // 2
    Dm = max(max(r) for r in d)
    L = np.array([[ (tr[i] if i == j else 0) - d[i][j] for j in range(n)] for i in range(n)], float)
    Q = np.array([[ (tr[i] if i == j else 0) + d[i][j] for j in range(n)] for i in range(n)], float)
    return L, Q, W, Dm

def is_path(n, rows):
    deg = [bin(r).count("1") for r in rows]
    return max(deg) <= 2 and sum(deg) // 2 == n - 1

def rayleigh(v, M):
    v = [F(x) for x in v]
    Mv = [sum(F(int(M[i][j])) * v[j] for j in range(len(v))) for i in range(len(v))]
    return sum(v[i] * Mv[i] for i in range(len(v))) / sum(x * x for x in v)

# ---------------------------------------------------------------- main census
def census(graphs, upto=7):
    rows_out = []
    margins = []
    for n in range(2, upto + 1):
        cnt = dl = dq = corr = diam5 = diam5_both = 0
        for rows in graphs[n]:
            d = distances(n, rows)
            L, Q, W, Dm = matrices(n, d)
            evL = np.sort(np.linalg.eigvalsh(L))[::-1]
            evQ = np.sort(np.linalg.eigvalsh(Q))[::-1]
            cnt += 1
            badL = badQ = False
            for k in range(1, n + 1):
                b = W + comb(k + 2, 3)
                if sum(evL[:k]) > b + 1e-9:
                    badL = True
                    margins.append(("DL", n, k, sum(evL[:k]) - b))
                if not is_path(n, rows) and sum(evQ[:k]) > b + 1e-9:
                    badQ = True
                    margins.append(("DQ", n, k, sum(evQ[:k]) - b))
            dl += badL
            dq += badQ
            if Dm == 5 and not is_path(n, rows):
                diam5 += 1
                diam5_both += (badL and badQ)
            for k in range(1, n + 1):
                c = W + Dm * comb(k + 1, 2)
                if sum(evL[:k]) > c + 1e-9 or sum(evQ[:k]) > c + 1e-9:
                    corr += 1
                    break
        rows_out.append((n, cnt, dl, dq, corr, diam5, diam5_both))
        print(f"n={n}: connected={cnt:3d} DL_viol={dl:2d} DQ_nonpath_viol={dq:2d} "
              f"corrected_viol={corr} diam5_nonpath={diam5} both={diam5_both}", flush=True)
    margins.sort(key=lambda t: t[3])
    print("smallest original-bound excesses:", [(a, b, c, round(x, 6)) for a, b, c, x in margins[:6]])
    return rows_out

# ---------------------------------------------------------------- certificates
CERT = {
    "P4   (DL,r=2)": (4, [(0, 1), (1, 2), (2, 3)], "L",
                      [[1, 0, 0, -1], [1, -1, -1, 1]], 2),
    "K13  (DL,r=2)": (4, [(0, 1), (0, 2), (0, 3)], "L",
                      [[0, 1, -1, 0], [0, 1, 1, -2]], 2),
    "P5   (DL,r=3)": (5, [(0, 1), (1, 2), (2, 3), (3, 4)], "L",
                      [[1, 0, 0, 0, -1], [0, 1, 0, -1, 0], [1, -1, 0, -1, 1]], 3),
    "B32  (DL,r=3)": (5, [(0, 1), (1, 2), (2, 3), (2, 4)], "L",
                      [[0, 0, 0, 1, -1], [2, -1, -1, 0, 0], [1, 1, 1, -1, -1]], 3),
    "B42  (DQ,k=3)": (6, [(0, 1), (1, 2), (2, 3), (3, 4), (3, 5)], "Q",
                      [[0, 0, 0, 0, 1, -1], [2, 1, 1, 1, 2, 2], [3, -2, 0, 0, -1, -1]], 3),
    "L33  (DQ,k=3)": (6, [(0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (4, 5)], "Q",
                      [[1, -1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 2], [1, 1, 0, 0, 2, -2]], 3),
}

def rows_from_edges(n, edges):
    rows = [0] * n
    for a, b in edges:
        rows[a] |= 1 << b
        rows[b] |= 1 << a
    return rows

def certificates():
    for name, (n, edges, kind, vecs, k) in CERT.items():
        rows = rows_from_edges(n, edges)
        d = distances(n, rows)
        L, Q, W, Dm = matrices(n, d)
        M = L if kind == "L" else Q
        quot = [rayleigh(v, M) for v in vecs]
        orth = all(sum(a * b for a, b in zip(v1, v2)) == 0
                   for i, v1 in enumerate(vecs) for v2 in vecs[:i])
        bound = W + comb(k + 2, 3)
        print(f"{name}: W={W} bound={bound} sum={sum(quot)} = {float(sum(quot)):.9f} "
              f"orthogonal={orth} strict={sum(quot) > bound}")

# ---------------------------------------------------------------- corrected bound stress test
def random_connected(n, rng, extra=0.0):
    while True:
        rows = [0] * n
        p = (1.0 + extra) / max(n - 1, 1)
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < p:
                    rows[i] |= 1 << j
                    rows[j] |= 1 << i
        if connected(n, rows):
            return tuple(rows)

def random_tree(n, rng):
    rows = [0] * n
    for v in range(1, n):
        u = int(rng.integers(0, v))
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return tuple(rows)

def stress(samples=400, nmax=13, seed=20261126):
    rng = np.random.default_rng(seed)
    checked = 0
    worst = []
    fails = []
    for n in range(8, nmax + 1):
        fam = [random_connected(n, rng) for _ in range(samples // 2)]
        fam += [random_tree(n, rng) for _ in range(samples // 2)]
        for rows in fam:
            d = distances(n, rows)
            L, Q, W, Dm = matrices(n, d)
            evL = np.sort(np.linalg.eigvalsh(L))[::-1]
            evQ = np.sort(np.linalg.eigvalsh(Q))[::-1]
            checked += 1
            for k in range(1, n + 1):
                c = W + Dm * comb(k + 1, 2)
                worst.append((c - sum(evL[:k]), n, k, "L"))
                worst.append((c - sum(evQ[:k]), n, k, "Q"))
                if sum(evL[:k]) > c + 1e-9 or sum(evQ[:k]) > c + 1e-9:
                    fails.append((n, k, rows))
    worst.sort()
    print(f"stress: {checked} graphs, corrected-bound failures: {len(fails)}")
    print("tightest corrected-bound margins:", [(round(m, 6), n, k, t) for m, n, k, t in worst[:8]])
    return fails

def sharper_bound_stress(samples=300, nmax=13, seed=20261127):
    """Test the conditional sharper bounds proposed in the phase-2 audit note:
         U_r <= W + (D-1)C(r+1,2) + n*min(r,n-1) - C(n,2)
         M_r^Q <= W + (D-1)C(r+1,2) + n + (n-2)r - C(n,2)
    They are strictly below W + D*C(r+1,2) for r < n-1, so they are a genuine
    strengthening *if* the derivation (ordinary Brouwer theorem + threshold
    decomposition) is correct. This only collects computational evidence.
    """
    rng = np.random.default_rng(seed)
    checked = fails = equal = 0
    worst = []
    for n in range(8, nmax + 1):
        fam = [random_connected(n, rng) for _ in range(samples // 2)]
        fam += [random_tree(n, rng) for _ in range(samples // 2)]
        for rows in fam:
            d = distances(n, rows)
            L, Q, W, Dm = matrices(n, d)
            evL = np.sort(np.linalg.eigvalsh(L))[::-1]
            evQ = np.sort(np.linalg.eigvalsh(Q))[::-1]
            checked += 1
            for k in range(1, n + 1):
                bL = W + (Dm - 1) * comb(k + 1, 2) + n * min(k, n - 1) - comb(n, 2)
                bQ = W + (Dm - 1) * comb(k + 1, 2) + n + (n - 2) * k - comb(n, 2)
                mL = bL - sum(evL[:k])
                mQ = bQ - sum(evQ[:k])
                worst.append((mL, "L", n, k))
                worst.append((mQ, "Q", n, k))
                if mL < -1e-9 or mQ < -1e-9:
                    fails += 1
                if abs(mL) < 1e-6 or abs(mQ) < 1e-6:
                    equal += 1
    worst.sort()
    print(f"sharper-bound lead: {checked} graphs, failures={fails}, "
          f"equality cases={equal}, tightest margins="
          f"{[(round(m, 4), t, n, k) for m, t, n, k in worst[:6]]}")
    return fails


# ---------------------------------------------------------------- families
def path_rows(n):
    return tuple((1 << (i - 1) if i > 0 else 0) | (1 << (i + 1) if i < n - 1 else 0) for i in range(n))

def broom_rows(n):
    # path on vertices 0..n-3, plus vertices n-2, n-1 attached to vertex n-3
    rows = list(path_rows(n - 2)) + [0, 0]
    rows[n - 3] |= (1 << (n - 2)) | (1 << (n - 1))
    rows[n - 2] = 1 << (n - 3)
    rows[n - 1] = 1 << (n - 3)
    return tuple(rows)

def lollipop_rows(n):
    # triangle on 0,1,2 then path 2-3-...-(n-1)
    rows = [0] * n
    rows[0] = (1 << 1) | (1 << 2)
    rows[1] = (1 << 0) | (1 << 2)
    rows[2] = (1 << 0) | (1 << 1) | (1 << 3)
    for v in range(3, n):
        if v + 1 < n:
            rows[v] = (1 << (v - 1)) | (1 << (v + 1))
        else:
            rows[v] = 1 << (v - 1)
    return tuple(rows)

def families(nmax=150):
    t_opt = 0.3660254037844386
    for label, gen, min_n in [("P_n", path_rows, 9), ("B(n-2,2)", broom_rows, 10), ("L(3,n-3)", lollipop_rows, 12)]:
        ratios = []
        ok = True
        for n in range(min_n, nmax + 1):
            rows = gen(n)
            d = distances(n, rows)
            L, Q, W, Dm = matrices(n, d)
            ev = np.sort(np.linalg.eigvalsh(L))[::-1]
            t = n // 3
            r = 2 * t
            U = sum(ev[:r])
            bound = W + comb(r + 2, 3)
            if U <= bound:
                ok = False
                print(f"  {label} n={n}: NO violation (U={U:.4f}, bound={bound})")
            if n >= 40:
                ratios.append((U - bound) / n ** 3)
        print(f"{label}: violations for all tested n={min_n}..{nmax}: {ok}; "
              f"excess/n^3 at n={nmax}: {ratios[-1]:.6f} (target 0.032692)")

# ---------------------------------------------------------------- sharper bound (Phase-II proposal)
def sharper_candidates(graphs, upto=7):
    """Test U_r <= W + (D-1)C(r+1,2) + n*min(r,n-1) - C(n,2) and the signless analogue."""
    worst = []
    fails = 0
    for n in range(2, upto + 1):
        for rows in graphs[n]:
            d = distances(n, rows)
            L, Q, W, Dm = matrices(n, d)
            evL = np.sort(np.linalg.eigvalsh(L))[::-1]
            evQ = np.sort(np.linalg.eigvalsh(Q))[::-1]
            for k in range(1, n + 1):
                bL = W + (Dm - 1) * comb(k + 1, 2) + n * min(k, n - 1) - comb(n, 2)
                bQ = W + (Dm - 1) * comb(k + 1, 2) + n + (n - 2) * k - comb(n, 2)
                worst.append((bL - sum(evL[:k]), "L", n, k))
                worst.append((bQ - sum(evQ[:k]), "Q", n, k))
                if sum(evL[:k]) > bL + 1e-9 or sum(evQ[:k]) > bQ + 1e-9:
                    fails += 1
    worst.sort()
    print(f"Phase-II sharper bound: {fails} failed (graph,k) cases on census; "
          f"tightest margins {[(round(m, 4), t, n, k) for m, t, n, k in worst[:5]]}")

if __name__ == "__main__":
    quick = "--quick" in sys.argv
    print("generating connected graphs ...")
    graphs = generate(7 if not quick else 6)
    print("census:")
    census(graphs, 7 if not quick else 6)
    print("published certificates:")
    certificates()
    print("corrected bound stress test:")
    stress(samples=200 if quick else 600, nmax=11 if quick else 13)
    print("Theta(n^3) families:")
    families(nmax=60 if quick else 150)
    if not quick:
        print("Phase-II sharper bound:")
        sharper_candidates(graphs, 7)
        print("Sharper-bound lead (random graphs):")
        sharper_bound_stress(samples=700, nmax=14)
