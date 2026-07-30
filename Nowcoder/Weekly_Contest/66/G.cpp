#include <vector>
#include <array>
#include <algorithm>
#include <iostream>
using namespace std;

using ll = long long;

vector<int> to_digits(ll x) {
    if (x == 0) return {0};
    vector<int> d;
    while (x > 0) {
        d.push_back(x % 10);
        x /= 10;
    }
    reverse(d.begin(), d.end());
    return d;
}

array<ll, 1 << 10> calc(ll N) {
    array<ll, 1 << 10> freq{};
    if (N < 0) return freq;
    auto digs = to_digits(N);
    int n = digs.size();


    vector<vector<vector<ll>>> dp(2, vector<vector<ll>>(2, vector<ll>(1 << 10, 0)));
    dp[1][0][0] = 1;

    for (int pos = 0; pos < n; ++pos) {
        vector<vector<vector<ll>>> ndp(2, vector<vector<ll>>(2, vector<ll>(1 << 10, 0)));
        for (int tight = 0; tight < 2; ++tight) {
            for (int started = 0; started < 2; ++started) {
                for (int mask = 0; mask < (1 << 10); ++mask) {
                    ll ways = dp[tight][started][mask];
                    if (ways == 0) continue;
                    int maxd = tight ? digs[pos] : 9;
                    for (int d = 0; d <= maxd; ++d) {
                        int ntight   = tight && (d == maxd);
                        int nstarted = started || (d != 0);
                        int nmask    = mask;
                        if (!started && d == 0) {
                        } else {
                            nmask = mask | (1 << d);
                        }
                        ndp[ntight][nstarted][nmask] += ways;
                    }
                }
            }
        }
        dp = move(ndp);
    }

 
    for (int tight = 0; tight < 2; ++tight) {
        for (int started = 0; started < 2; ++started) {
            for (int mask = 0; mask < (1 << 10); ++mask) {
                ll ways = dp[tight][started][mask];
                if (ways == 0) continue;
                int final_mask = started ? mask : (1 << 0);
                freq[final_mask] += ways;
            }
        }
    }
    return freq;
}

void solve() {
    ll x, k;
    cin >> x >> k;
    ll L = x, R = x + k;
    auto freqR = calc(R);
    auto freqL = calc(L - 1);

    int max_mex = 0;
    ll cnt = 0;
    for (int mask = 0; mask < (1 << 10); ++mask) {
        ll num = freqR[mask] - freqL[mask];
        if (num <= 0) continue;
        int mex = 0;
        while (mex < 10 && (mask & (1 << mex))) ++mex;

        if (mex > max_mex) {
            max_mex = mex;
            cnt = num;
        } else if (mex == max_mex) {
            cnt += num;
        }
    }
    cout << max_mex << ' ' << cnt << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    cin >> T;
    while (T--) solve();
    return 0;
}