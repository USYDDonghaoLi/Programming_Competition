#include <iostream>
#include <vector>

using namespace std;

const int mod = 998244353;

int main(){
    int n, m;
    cin >> n >> m;

    vector<int> A(n);

    for (int i = 0; i < n; i++) {
        cin >> A[i];
    }

    vector<vector<int>> adj(n);

    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        --u;
        --v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    long long res = 0;

    for (int u = 0; u < n; u++) {
        vector<int> B(30, 0);
        for (int v: adj[u]){
            for (int bit = 0; bit < 30; bit++) {
                if (A[v] & (1 << bit)) {
                    ++B[bit];
                }
            }
        }

        int k = adj[u].size();
        for (int bit = 0; bit < 30; bit++) {
            int one = B[bit];
            int zero = k - one;
            int cur = A[u] >> bit & 1;
            if (!cur) {
                long long tmp = 1LL * one * zero;
                tmp %= mod;
                res += (1LL << bit) * tmp % mod;
            } else {
                long long tmp = 1LL * one * (one - 1) / 2 + 1LL * zero * (zero - 1) / 2;
                tmp %= mod;
                res += (1LL << bit) * tmp % mod;
            }
            res %= mod;
        }
    }

    cout << res << "\n";

}