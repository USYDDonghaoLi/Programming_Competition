#include <bits/stdc++.h>
using namespace std;

#define INF (2e9+10)
#define int long long

// Optimized input
void fast_io() {
    ios::sync_with_stdio(false);
    cin.tie(0);
}

// Function to solve each test case
void solve() {
    int n;
    cin >> n;

    vector<int> A(n), P(n);
    for (int &x : A) cin >> x;
    for (int i = 1; i < n; ++i) cin >> P[i], P[i]--;

    vector<vector<int>> child(n);
    for (int i = 1; i < n; ++i) {
        child[P[i]].push_back(i);
    }

    vector<int> depth(n, 0);
    queue<int> q;
    q.push(0);

    while (!q.empty()) {
        int cur = q.front();
        q.pop();
        for (int o : child[cur]) {
            depth[o] = depth[cur] + 1;
            q.push(o);
        }
    }

    auto check = [&](int mid) -> bool {
        if (A[0] >= mid) return true;
        vector<int> B = A;

        queue<pair<int, int>> q;
        for (int o : child[0]) {
            q.emplace(o, mid - B[0]);
        }

        while (!q.empty()) {
            auto [cur, need] = q.front();
            q.pop();
            B[cur] -= need;
            if (B[cur] + INF < 0){
                return false;
            }

            if (child[cur].empty()) {
                if (B[cur] < 0) return false;
            }

            int new_need = B[cur] >= 0 ? 0 : -B[cur];
            for (int o : child[cur]) {
                q.emplace(o, need + new_need);
            }
        }
        return true;
    };

    int l = 0, r = INF;
    while (l < r) {
        int mid = (l + r) >> 1;
        if (check(mid)) {
            l = mid + 1;
        } else {
            r = mid;
        }
    }
    cout << l - 1 << '\n';
}

signed main() {
    fast_io();
    int t;
    cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}
