#include <cstring>
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <set>
#include <tuple>
#include <cstdint>

// Fast enumeration of ALL connected simple graphs on n=7 vertices (up to isomorphism via canonical BFS/DFS/spectrum+degree+distance-multiset).
// Actually we output the exact edge masks of all unique non-isomorphic connected graphs on n=7 (853 graphs) by canonicalizing with n<=7!
// Wait: 7! = 5040 is tiny, so we can deduplicate by a fast invariant (sorted degs, sorted transmissions, Wiener, diam, sorted distance pairs)
// AND verify isomorphism via 7! permutation check only on hash collisions!

using namespace std;

const int N = 7;
int edges_u[21], edges_v[21];

uint64_t canonical_code(int adj[N][N]) {
    // Only called on unique invariant buckets if needed; here we use a fast 64-bit invariant first
    return 0;
}

bool are_isomorphic(const int A[N][N], const int B[N][N], const int degA[N], const int degB[N]) {
    int p[N] = {0,1,2,3,4,5,6};
    do {
        bool ok = true;
        for (int i = 0; i < N; ++i) {
            if (degA[i] != degB[p[i]]) { ok = false; break; }
        }
        if (!ok) continue;
        for (int i = 0; i < N && ok; ++i)
            for (int j = i + 1; j < N; ++j)
                if (A[i][j] != B[p[i]][p[j]]) { ok = false; break; }
        if (ok) return true;
    } while (next_permutation(p, p + N));
    return false;
}

#include <unordered_map>

struct GraphRep {
    int adj[N][N];
    int deg[N];
    uint32_t mask;
};

int main() {
    int idx = 0;
    for (int i = 0; i < N; ++i)
        for (int j = i + 1; j < N; ++j) {
            edges_u[idx] = i;
            edges_v[idx] = j;
            idx++;
        }

    unordered_map<uint64_t, vector<GraphRep>> buckets;
    buckets.reserve(4096);
    int total_unique = 0;

    for (uint32_t mask = 0; mask < (1u << 21); ++mask) {
        if (__builtin_popcount(mask) < N - 1) continue;
        int adj[N][N] = {0};
        int deg[N] = {0};
        for (int e = 0; e < 21; ++e) {
            if ((mask >> e) & 1) {
                int u = edges_u[e], v = edges_v[e];
                adj[u][v] = adj[v][u] = 1;
                deg[u]++; deg[v]++;
            }
        }
        // Quick connectivity check via BFS
        int q[N], vis = 1, head = 0, tail = 0;
        q[tail++] = 0;
        while (head < tail) {
            int u = q[head++];
            for (int v = 0; v < N; ++v) {
                if (adj[u][v] && !((vis >> v) & 1)) {
                    vis |= (1 << v);
                    q[tail++] = v;
                }
            }
        }
        if (tail < N) continue;

        // Fast isomorphism-invariant hash: sorted degree seq + sorted 2-hop deg sums + triangle counts
        uint64_t h = 0;
        int sig[N];
        for (int i = 0; i < N; ++i) {
            int s2 = 0, tri = 0;
            for (int j = 0; j < N; ++j) if (adj[i][j]) {
                s2 += deg[j];
                for (int k = j + 1; k < N; ++k) if (adj[i][k] && adj[j][k]) tri++;
            }
            sig[i] = (deg[i] << 12) | (s2 << 5) | tri;
        }
        sort(sig, sig + N);
        for (int i = 0; i < N; ++i) h = h * 1000003ULL + (uint64_t)sig[i];

        auto &vec = buckets[h];
        bool dup = false;
        for (const auto &g : vec) {
            if (are_isomorphic(adj, g.adj, deg, g.deg)) {
                dup = true;
                break;
            }
        }
        if (!dup) {
            GraphRep gr;
            memcpy(gr.adj, adj, sizeof(adj));
            memcpy(gr.deg, deg, sizeof(deg));
            gr.mask = mask;
            vec.push_back(gr);
            total_unique++;
        }
    }

    cerr << "Total unique connected graphs on n=7: " << total_unique << endl;
    for (const auto &kv : buckets) {
        for (const auto &g : kv.second) {
            cout << g.mask << "\n";
        }
    }
    return 0;
}
