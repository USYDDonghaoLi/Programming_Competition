#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <numeric>
#include <functional>
#include <iterator>
#include <ctime>
#include <cstdlib>
#include <map>
#include <set>
#include <string>
#include <cstring>
#include <queue>
#include <stack>
#include <tuple>
#include <unordered_map>
#include <unordered_set>

using namespace std;

#define int long long
const int mod = 998244353;

class Factorial {
public:
    Factorial(int N, int mod) : mod(mod) {
        f.resize(N);
        g.resize(N);
        f[0] = 1;
        for (int i = 1; i < N; i++) {
            f[i] = f[i - 1] * i % mod;
        }
        g[N - 1] = power(f[N - 1], mod - 2);
        for (int i = N - 2; i >= 0; i--) {
            g[i] = g[i + 1] * (i + 1) % mod;
        }
    }

    int comb(int n, int m) {
        if (n < m || n < 0 || m < 0) {
            return 0;
        }
        return f[n] * g[m] % mod * g[n - m] % mod;
    }

    int perm(int n, int m) {
        if (n < m || n < 0 || m < 0) {
            return 0;
        }
        return f[n] * g[n - m] % mod;
    }

    int catalan(int n) {
        return (comb(2 * n, n) - comb(2 * n, n - 1)) % mod;
    }

    int power(int x, int y) {  // Made this function public
        int res = 1;
        while (y > 0) {
            if (y % 2 == 1) {
                res = res * x % mod;
            }
            x = x * x % mod;
            y /= 2;
        }
        return res;
    }

private:
    vector<int> f, g;
    int mod;
};

Factorial F(1010, mod);

void solve() {
    int n;
    cin >> n;
    vector<int> C(26);
    for (int i = 0; i < 26; ++i) {
        cin >> C[i];
    }

    // for (int i = 0; i < 26; i++){
    //     cout << C[i] << " \n"[i == 25];
    // }

    vector<int> res(n + 1, 0);
    res[0] = 1;
    int final = 0;

    for (const auto& c : C) {
        if (!c) continue;
        vector<int> new_res(n + 1, 0);
        for (int i = 0; i <= n; ++i) {
            for (int j = 0; j <= c; ++j) {
                if (i + j > n) break;
                new_res[i + j] = (new_res[i + j] + res[i] * F.comb(n - i, j) % mod) % mod;
            }
        }
        swap(res, new_res);
        // for (int i = 0; i <= n; i++){
        //     cout << res[i] << " \n"[i == n];
        // }
    }

    for (int i = 1; i <= n; ++i) {
        final = (final + res[i] * F.power(F.comb(n, i), mod - 2) % mod) % mod;
    }

    cout << final << "\n";
}

int32_t main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    int t = 1;
    // cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}
