#pragma GCC optimize(1)
#pragma GCC optimize(2)
#pragma GCC optimize(3,"Ofast","inline")
#include<bits/stdc++.h>
using namespace std;

long long quickpow(long long a, long long b, long long mod){
    long long ans;
    for (ans = 1; b; b >>= 1){
        if (b & 1){
            ans = (ans * a) % mod;
        }
        a = (a * a) % mod;
    }
    return ans;
}

template <class T>
void chmin(T &a, T b){
    if (b < a) a = b;
}
template <class T>
void chmax(T &a, T b){
    if (b > a) a = b;
}

const int inf = 0x3f3f3f3f;
const long long infl = 0x3f3f3f3f3f3f3f3f;

int dir[4][2] = {1, 0, -1, 0, 0, -1, 0, 1};
const long long mod = 998244353;

void solve(int testcase){
    int n, m, k;
    cin >> n >> m >> k;
    
    vector<vector<long long>> adj(n);
    for (int i = 0; i < m; i++){
        int u, v;
        cin >> u >> v;
        --u, --v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    vector<long long> dp(n, 0);
    dp[0] = 1;

    for (int _ = 0; _ < k; _++){
        vector<long long> dp2(n);
        long long s = 0;
        for (int i = 0; i < n; i++){
            s += dp[i];
            for (int o: adj[i]){
                dp2[o] -= dp[i];
            }
        }
        for (int i = 0; i < n; i++){
            dp[i] = (dp2[i] + s - dp[i]) % mod;
        }
    }
    
    cout << dp[0] << "\n";

}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0); cout.tie(0);
    int T = 1;
    //cin >> T;
    for (int testcase = 1; testcase <= T; testcase++) solve(testcase);
    return 0;
}