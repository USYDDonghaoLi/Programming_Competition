#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100010;

void dfs(int u, int fa, int k, vector<vector<int>>& adj, vector<long long>& A, vector<int>& leaves, vector<vector<long long>>& dp) {
    int cnt = 0;
    for (int v : adj[u]) {
        if (v != fa) {
            cnt++;
            dfs(v, u, k, adj, A, leaves, dp);
            leaves[u] += leaves[v];
        }
    }
    if (cnt == 0) {
        leaves[u] = 1;
    }
    
    dp[u].resize(min(leaves[u], k) + 1, 0);

    int cur = 0;
    for (int v : adj[u]) {
        if (v != fa) {
            vector<long long> new_dp(min(leaves[u], k) + 1, 0);
            for (int i = 0; i <= cur && i <= k; i++) {
                for (int j = 0; j <= min(leaves[v], k) && i + j <= k; j++) {
                    new_dp[i + j] = max(new_dp[i + j], dp[u][i] + dp[v][j]);
                }
            }
            for (int i = 0; i <= min(leaves[u], k); i++) {
                dp[u][i] = new_dp[i];
            }
            cur += leaves[v];
        }
    }
    if (leaves[u] <= k) {
        dp[u][leaves[u]] += A[u];
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    int n, k;
    cin >> n >> k;
    vector<long long> A(n);
    for (int i = 0; i < n; i++) {
        cin >> A[i];
    }
    vector<vector<int>> adj(n);
    vector<int> leaves(n, 0);
    vector<vector<long long>> dp(n);

    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        u--; v--; // Adjust to 0-based indexing
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    dfs(0, -1, k, adj, A, leaves, dp);
    cout << dp[0][k] << '\n';

    return 0;
}