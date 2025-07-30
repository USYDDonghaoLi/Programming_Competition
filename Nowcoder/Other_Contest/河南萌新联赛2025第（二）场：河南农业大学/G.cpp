#include<iostream>
#include<vector>
using namespace std;

int main(){
    cin.tie(0);

    int n, k;
    cin >> n >> k;

    vector<int> A(n, 0);
    for (int i = 0; i < n; i++){
        cin >> A[i];
    }

    vector<int> leaves(n, 0);
    vector<vector<int>> mp(n);
    vector<vector<int>> adj(n);

    for (int i = 0; i < n - 1; i++){
        int u, v;
        cin >> u >> v;
        --u;
        --v;
        adj[u].emplace_back(v);
        adj[v].emplace_back(u);
    }

    auto dfs = [&](auto &&self, int u, int fa) -> void {
        int cnt = 0;
        for (auto v: adj[u]){
            if (v != fa){
                ++cnt;
                self(self, v, u);
                leaves[u] += leaves[v];
            }
        }

        if (!cnt){
            leaves[u] = 1;
        }

        mp[u].resize(min(k, leaves[u]) + 1, 0);

        int cur = 0;

        for (auto v: adj[u]){
            if (v != fa){
                for (int i = cur; i >= 0; --i){
                    for (int j = 0; j <= leaves[v]; ++j){
                        if (i + j >= mp[u].size()){
                            break;
                        }
                        mp[u][i + j] = min(mp[u][i + j], mp[u][i] + mp[v][j]);
                    }
                }
                cur += leaves[v];
            }
        }

        if (leaves[u] < mp[u].size()){
            mp[u][leaves[u]] += A[u];
        }


    };

    dfs(dfs, 0, -1);

    cout << mp[0][k] << "\n";

    return 0;
}