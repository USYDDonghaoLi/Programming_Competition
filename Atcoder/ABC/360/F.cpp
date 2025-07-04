#include <bits/stdc++.h>
#include <atcoder/lazysegtree>
using namespace std;

int op(int a, int b) {
    return max(a, b);
}
int e() {
    return 0;
}
int mapping(int f, int x) {
    return x + f;
}
int composition(int f, int g) {
    return f + g;
}
int id() {
    return 0;
}

int main() {
    int n;
    cin >> n;
    vector<int> L(n), R(n);
    for (int i = 0; i < n; ++i) {
        cin >> L[i] >> R[i];
    }

    // 座標圧縮
    vector<int> press;
    {
        for (int i = 0; i < n; ++i) {
            press.emplace_back(L[i] + 1);
            press.emplace_back(R[i] + 1);
            press.emplace_back(R[i]);
        }
        press.emplace_back(0);
        press.emplace_back(1'000'000'000);
        sort(press.begin(), press.end());
        press.erase(unique(press.begin(), press.end()), press.end());
        while (press.back() > 1'000'000'000) press.pop_back();
    }
    auto get = [&press](int x) -> int {
        return lower_bound(press.begin(), press.end(), x) - press.begin();
    };

    // 矩形領域を求める
    vector<array<int, 4>> query;
    for (int i = 0; i < n; ++i) {
        if (R[i] + 1 < 1'000'000'000) {
            query.push_back({L[i] + 1, 1, get(R[i] + 1), (int)press.size()});
            query.push_back({R[i], -1, get(R[i] + 1), (int)press.size()});
        }
        if (L[i] > 0 && L[i] + 1 < R[i]) {
            query.push_back({0, 1, get(L[i] + 1), get(R[i])});
            query.push_back({L[i], -1, get(L[i] + 1), get(R[i])});
        }
    }
    sort(query.begin(), query.end());

    atcoder::lazy_segtree<int, op, e, int, mapping, composition, id> seg(vector<int>(press.size(), 0));

    // 平面走査
    int ma = 0;
    int l = 0, r = 1;
    int idx = 0;
    while (idx < (int)query.size()) {
        const int now = query[idx][0];
        while (idx < (int)query.size() && query[idx][0] == now) {
            seg.apply(query[idx][2], query[idx][3], query[idx][1]);
            ++idx;
        }
        auto val = seg.all_prod();
        if (val > ma) {
            ma = val;
            l = now;
            int idx = seg.max_right(0, [&](int x) { return x < ma; });
            r = press[idx];
        }
    }

    cout << l << ' ' << r << '\n';
}