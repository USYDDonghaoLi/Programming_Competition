// #pragma GCC optimize("O3,unroll-loops")
// #pragma GCC target("avx2,bmi,bmi2,lzcnt,popcnt")
#include "bits/stdc++.h"
using namespace std;
using ll = long long int;
mt19937_64 rng(chrono::high_resolution_clock::now().time_since_epoch().count());

int main()
{
    ios::sync_with_stdio(false); cin.tie(0);

    const int maxA = 1e7 + 10;
    const int mod = 998244353;
    vector<int> spf(maxA), sqfree(maxA);
    for (int i = 2; i < maxA; ++i) {
        if (spf[i]) continue;
        for (int j = i; j < maxA; j += i)
            if (!spf[j]) spf[j] = i;
    }
    sqfree[1] = 1;
    for (int i = 2; i < maxA; ++i) {
        int p = spf[i];
        if (spf[i/p] == p) sqfree[i] = sqfree[(i/p)/p];
        else sqfree[i] = p*sqfree[i/p];
    }

    vector<ll> lensum(maxA);
    int t; cin >> t;
    while (t--) {
        int n; cin >> n;
        vector<int> a(n);
        for (int &x : a) cin >> x;
        vector<map<int, int>> end_gcd(n), start_gcd(n);
        ll ans = 0;
        for (int i = 0; i < n; ++i) {
            end_gcd[i][a[i]] = 0;
            if (i) for (auto &[x, y] : end_gcd[i-1]) {
                int g = gcd(x, a[i]);
                end_gcd[i][g] = max(end_gcd[i][g], y + 1);
            }

            // for (auto& [x, y]: end_gcd[i]){
            //     cout << x << " " << y << "\n";
            // }
            // cout << "\n";
        }
            
        
        for (int i = n-1; i >= 0; --i) {
            auto it = begin(end_gcd[i]);
            while (it != end(end_gcd[i])) {
                auto [x, y] = *it;
                cout << x << " " << y << "xy\n";
                int pos = sqfree[x];

                int len = 0;
                if (next(it) != end(end_gcd[i])) {
                    auto [x2, y2] = *next(it);
                    len = y - y2;
                }
                else {
                    len = y+1;
                }
                cout << len << "len\n";
                ans += (len * lensum[pos] % mod) % mod;
                ++it;
                cout << "ans " << ans << "\n";
            }
            

            start_gcd[i][a[i]] = 0;
            if (i+1 < n) for (auto &[x, y] : start_gcd[i+1]) {
                int g = gcd(x, a[i]);
                start_gcd[i][g] = max(start_gcd[i][g], y + 1);
            }
            auto it2 = begin(start_gcd[i]);
            while (it2 != end(start_gcd[i])) {
                auto [x, y] = *it2;
                int pos = sqfree[x];
                if (next(it2) != end(start_gcd[i])) {
                    auto [x2, y2] = *next(it2);
                    lensum[pos] += y - y2;
                }
                else {
                    lensum[pos] += y + 1;
                }
                ++it2;
            }
        }
        for (int i = 0; i < n; ++i) for (auto &[x, y] : start_gcd[i])
            lensum[sqfree[x]] = 0;
        cout << ans%mod << '\n';
    }
}