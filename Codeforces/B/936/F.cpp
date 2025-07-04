#include <bits/stdc++.h>
using namespace std;

// Fenwick Tree or Binary Indexed Tree
class FenwickTree {
public:
    vector<long long> tree;
    long long n;

    FenwickTree(long long _n) : n(_n), tree(_n + 1, 0) {}

    // Single element update
    void update(long long idx, long long delta) {
        for (++idx; idx <= n; idx += idx & -idx)
            tree[idx] += delta;
    }

    // Prefix sum query
    long long query(long long idx) {
        long long sum = 0;
        for (++idx; idx > 0; idx -= idx & -idx)
            sum += tree[idx];
        return sum;
    }

    // Range sum query
    long long queryRange(long long l, long long r) {
        return query(r) - query(l - 1);
    }
};

void solve() {
    long long n, q;
    cin >> n >> q;
    vector<long long> A(n);
    for (long long& a : A) cin >> a;

    vector<vector<pair<int, int>>> queries(n + 1);
    for (int i = 0; i < q; ++i) {
        int a, b;
        cin >> a >> b;
        queries[a].emplace_back(b, i);
    }

    vector<int> ID(n + 1, -1);
    for (int i = 0; i < n; ++i)
        ID[A[i]] = i + 1;

    vector<long long> res(q, -1), to_add(n + 1, 0);
    FenwickTree ft(n + 10);

    for (int i = n - 1; i >= 0; --i) {
        long long x = A[i];
        to_add[x] = 1;

        for (long long v = x; v <= n; v += x) {
            ft.update(ID[v], to_add[v]);
            for (long long u = v + v; u <= n; u += v)
                if (ID[v] < ID[u])
                    to_add[u] += to_add[v];
            to_add[v] = 0;
        }

        for (auto& [r, idx] : queries[i + 1])
            res[idx] = ft.queryRange(i + 1, r);
    }

    for (long long r : res)
        cout << r << " ";
    cout << "\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--)
        solve();

    return 0;
}
