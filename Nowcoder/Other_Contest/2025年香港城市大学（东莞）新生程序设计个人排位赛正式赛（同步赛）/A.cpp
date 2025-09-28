#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<ll, ll>;

pii get_v(char c) {
    if (c == 'U') return {0, 1};
    if (c == 'D') return {0, -1};
    if (c == 'L') return {-1, 0};
    if (c == 'R') return {1, 0};
    return {0, 0};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    string s;
    cin >> s;

    vector<pii> pos(n + 1, {0, 0});
    for (int i = 1; i <= n; ++i) {
        pii v = get_v(s[i - 1]);
        pos[i] = {pos[i - 1].first + v.first, pos[i - 1].second + v.second};
    }

    map<pii, int> min_k, last_k;
    for (int i = 1; i <= n; ++i) {
        auto p = pos[i];
        if (!min_k.count(p)) min_k[p] = i;
        last_k[p] = i;
    }

    vector<vector<int>> A(4);
    map<char, int> B = {{'U', 0}, {'D', 1}, {'L', 2}, {'R', 3}};
    for (int j = 1; j <= n; ++j) {
        char c = s[j - 1];
        A[B[c]].push_back(j);
    }

    array<int, 4> cnt = {0, 0, 0, 0};
    for (char c : s) ++cnt[B[c]];

    ll dx = cnt[3] - cnt[2];
    ll dy = cnt[0] - cnt[1];
    bool has_h = (cnt[2] + cnt[3] > 0);
    bool has_v = (cnt[0] + cnt[1] > 0);

    vector<string> dirs = {"U", "D", "L", "R"};

    for (int iq = 0; iq < q; ++iq) {
        ll px, py;
        cin >> px >> py;
        pii pit = {px, py};

        bool visits_orig = min_k.count(pit);
        if (!visits_orig) {
            cout << 0 << '\n';
            continue;
        }
        int kmin = min_k[pit];

        bool flag = false;
        if (!has_v) {
            if (py != 0) flag = false;
            else flag = ((px > 0 && dx >= px) || (px < 0 && dx <= px));
        } else if (!has_h) {
            if (px != 0) flag = false;
            else flag = ((py > 0 && dy >= py) || (py < 0 && dy <= py));
        } else {
            flag = (px == dx && py == dy);
        }

        if (!flag) {
            cout << 1 << '\n';
            continue;
        }

        bool flag2 = false;
        for (char oldc : {'U', 'D', 'L', 'R'}) {
            for (char newc : {'U', 'D', 'L', 'R'}) {
                if (oldc == newc) continue;
                pii dv = get_v(newc);
                pii ov = get_v(oldc);
                pii delta = {dv.first - ov.first, dv.second - ov.second};
                pii t = {px - delta.first, py - delta.second};

                int last = 0;
                auto it = last_k.find(t);
                if (it != last_k.end()) last = it->second;

                int sj = last + 1;
                if (sj > kmin) continue;

                int idx = B[oldc];
                auto& lis = A[idx];
                auto iter = lower_bound(lis.begin(), lis.end(), sj);
                if (iter != lis.end() && *iter <= kmin) {
                    flag2 = true;
                    break;
                }
            }
            if (flag2) break;
        }

        if (flag2) cout << 1 << '\n';
        else cout << 2 << '\n';
    }

    return 0;
}