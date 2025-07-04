#include <bits/stdc++.h>
using namespace std;

#define int long long
#define MAXN 200010
#define INF 1e18

class FastIO {
public:
    FastIO() {
        ios::sync_with_stdio(0);
        cin.tie(0);
    }
};

class LCA {
public:
    int n, m;
    vector<vector<int>> fa;
    vector<int> depth;
    vector<vector<int>> graph, child;

    LCA(int n) : n(n), m(log2(n) + 1), fa(n, vector<int>(m, -1)), depth(n, INF), graph(n), child(n) {}

    void addEdge(int a, int b) {
        graph[a].push_back(b);
        graph[b].push_back(a);
    }

    void bfs(int root) {
        depth[root] = 0;
        queue<int> q;
        q.push(root);
        for (int k = 0; k < m; ++k) {
            fa[root][k] = root;
        }

        while (!q.empty()) {
            int cur = q.front(); q.pop();
            for (int e : graph[cur]) {
                if (depth[e] > depth[cur] + 1) {
                    child[cur].push_back(e);
                    depth[e] = depth[cur] + 1;
                    q.push(e);
                    fa[e][0] = cur;
                    for (int i = 1; i < m; ++i) {
                        fa[e][i] = fa[fa[e][i - 1]][i - 1];
                    }
                }
            }
        }
    }

    int sol(int a, int b) {
        if (depth[a] < depth[b]) {
            swap(a, b);
        }
        for (int k = m - 1; k >= 0; --k) {
            if (depth[fa[a][k]] >= depth[b]) {
                a = fa[a][k];
            }
        }
        if (a == b) return a;
        for (int k = m - 1; k >= 0; --k) {
            if (fa[a][k] != fa[b][k]) {
                a = fa[a][k];
                b = fa[b][k];
            }
        }
        return fa[a][0];
    }

    vector<int> routes(int a, int b) {
        int p = sol(a, b);
        vector<int> aroute, broute;
        int cur = a;
        while (cur != p) {
            aroute.push_back(cur);
            cur = fa[cur][0];
        }
        cur = b;
        while (cur != p) {
            broute.push_back(cur);
            cur = fa[cur][0];
        }
        aroute.push_back(p);
        aroute.insert(aroute.end(), broute.rbegin(), broute.rend());
        return aroute;
    }
};

int32_t main() {
    FastIO io;

    int n;
    cin >> n;
    LCA L(n);
    unordered_map<int, vector<int>> mp;
    vector<vector<int>> adj(n);
    
    for (int i = 0; i < n - 1; ++i) {
        int u, v;
        cin >> u >> v;
        --u; --v;
        L.addEdge(u, v);
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    
    L.bfs(0);
    
    vector<int> A(n);
    for (int i = 0; i < n; ++i) {
        cin >> A[i];
        mp[A[i]].push_back(i);
    }
        
    auto calc = [&](int v) {
        vector<int> TOT(n, 0), CNT(n, 0), RES(n, 0);

        function<void(int, int)> dfs = [&](int cur, int fa) {
            int tot = 0, cnt = 0, res = 0;
            vector<int> lst, lst2;

            for (int o : adj[cur]) {
                if (o == fa) continue;
                dfs(o, cur);
                int tot_son = TOT[o], cnt_son = CNT[o], res_son = RES[o];
                int tmp = tot_son + cnt_son;
                tot += tmp;
                cnt += cnt_son;
                lst.push_back(tmp);
                lst2.push_back(cnt_son);
                res += res_son;
            }

            for (size_t i = 0; i < lst.size(); ++i) {
                res += lst[i] * (cnt - lst2[i]);
            }

            if (A[cur] == v) {
                cnt += 1;
                res += tot;
            }

            TOT[cur] = tot;
            CNT[cur] = cnt;
            RES[cur] = res;
        };

        dfs(0, -1);
        return RES[0];
    };

    int res = 0;
    for (auto &p : mp) {
        int v = p.first;
        int m = p.second.size();
        if (m <= 150) {
            for (int i = 0; i < m; ++i) {
                int a = p.second[i];
                for (int j = i + 1; j < m; ++j) {
                    int b = p.second[j];
                    int c = L.sol(a, b);
                    res += L.depth[a] + L.depth[b] - 2 * L.depth[c];
                }
            }
        } else {
            res += calc(v);
        }
    }

    cout << res << endl;

    return 0;
}
