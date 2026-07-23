#include <bits/stdc++.h>
using namespace std;

#define int long long
const int inf = 1e18;

struct SegTree {
    int n;
    vector<array<int, 7>> d;
    function<array<int, 7>(array<int, 7>, array<int, 7>)> op;
    array<int, 7> e;
    
    SegTree(const vector<int> &V, function<array<int, 7>(array<int, 7>, array<int, 7>)> OP, array<int, 7> E) {
        n = V.size();
        op = OP;
        e = E;
        d.resize(2 * n, E);
        for (int i = 0; i < n; ++i)
            d[n + i] = {V[i], V[i], V[i], V[i], V[i], V[i], V[i]};
        for (int i = n - 1; i > 0; --i)
            update(i);
    }
    
    void set(int p, array<int, 7> x) {
        for (d[p += n] = x; p /= 2;)
            update(p);
    }
    
    array<int, 7> get(int p) {
        return d[p + n];
    }
    
    array<int, 7> prod(int l, int r) {
        array<int, 7> sml = e, smr = e;
        for (l += n, r += n; l < r; l /= 2, r /= 2) {
            if (l & 1) sml = op(sml, d[l++]);
            if (r & 1) smr = op(d[--r], smr);
        }
        return op(sml, smr);
    }
    
    void update(int k) {
        d[k] = op(d[2 * k], d[2 * k + 1]);
    }
    
    string toString() {
        stringstream ss;
        ss << "[";
        for (int i = 0; i < n; ++i) {
            if (i > 0) ss << ", ";
            ss << get(i)[0];
        }
        ss << "]";
        return ss.str();
    }
};

array<int, 7> combine(array<int, 7> x, array<int, 7> y) {
    return {
        x[0] + y[0],
        max(x[1], x[0] + y[1]),
        min(x[2], x[0] + y[2]),
        max(y[3], y[0] + x[3]),
        min(y[4], y[0] + x[4]),
        max({x[5], y[5], x[3] + y[1]}),
        min({x[6], y[6], x[4] + y[2]})
    };
}

signed main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i)
        cin >> nums[i];
    
    SegTree sg(nums, combine, {0, -inf, inf, -inf, inf, -inf, inf});
    
    int q;
    cin >> q;
    while (q--) {
        int l, r;
        cin >> l >> r;
        --l; --r;
        auto res = sg.prod(l, r + 1);
        cout << max(abs(res[5]), abs(res[6])) << "\n";
    }
    
    return 0;
}
