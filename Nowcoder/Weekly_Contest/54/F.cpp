#include <iostream>
#include <vector>
#include <stack>

using namespace std;

using ll = long long;

const int MAXN = 1000005;

int n, m, N;
vector<int> g[MAXN];
int val[MAXN];
int dfn[MAXN], low[MAXN], timer;
stack<int> stk;
bool in_stk[MAXN];
vector<vector<int>> bccs;
vector<int> tree[MAXN * 2];
vector<int> members[MAXN];
int parent[MAXN * 2];
bool vis[MAXN * 2];

int dx[4] = {-1, 1, 0, 0};
int dy[4] = {0, 0, -1, 1};

void tarjan(int u, int fa) {
    dfn[u] = low[u] = ++timer;
    stk.push(u);
    in_stk[u] = true;
    for (int v : g[u]) {
        if (v == fa) continue;
        if (!dfn[v]) {
            tarjan(v, u);
            low[u] = min(low[u], low[v]);
            if (low[v] >= dfn[u]) {
                vector<int> comp;
                while (true) {
                    int x = stk.top(); stk.pop();
                    in_stk[x] = false;
                    comp.push_back(x);
                    if (x == v) break;
                }
                comp.push_back(u);
                bccs.push_back(comp);
            }
        } else if (in_stk[v]) {
            low[u] = min(low[u], dfn[v]);
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m;
    N = n * m;
    vector<vector<int>> a(n, vector<int>(m));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> a[i][j];
            int u = i * m + j;
            if (a[i][j] != -1) val[u] = a[i][j];
        }
    }

    // 建图
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (a[i][j] == -1) continue;
            int u = i * m + j;
            for (int d = 0; d < 4; d++) {
                int ni = i + dx[d], nj = j + dy[d];
                if (ni >= 0 && ni < n && nj >= 0 && nj < m && a[ni][nj] != -1) {
                    int v = ni * m + nj;
                    if (u < v) {
                        g[u].push_back(v);
                        g[v].push_back(u);
                    }
                }
            }
        }
    }

    int S = 0, T = N - 1;

    // Tarjan（只处理 S 所在连通分量）
    timer = 0;
    tarjan(S, -1);

    // 处理栈中剩余
    if (!stk.empty()) {
        if (bccs.empty()) {
            vector<int> comp;
            while (!stk.empty()) {
                int x = stk.top(); stk.pop();
                in_stk[x] = false;
                comp.push_back(x);
            }
            bccs.push_back(comp);
        } else {
            while (!stk.empty()) {
                in_stk[stk.top()] = false;
                stk.pop();
            }
        }
    }

    // 建圆方树
    int sq_cnt = bccs.size();
    for (int i = 0; i < sq_cnt; i++) {
        int sq = N + i;
        members[i] = bccs[i];
        for (int x : bccs[i]) {
            tree[x].push_back(sq);
            tree[sq].push_back(x);
        }
    }

    if (!dfn[T]) {
        cout << 0 << "\n";
        return 0;
    }

    // BFS 求路径
    queue<int> q;
    q.push(S);
    vis[S] = true;
    parent[S] = S;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        if (u == T) break;
        for (int v : tree[u]) {
            if (!vis[v]) {
                vis[v] = true;
                parent[v] = u;
                q.push(v);
            }
        }
    }

    if (!vis[T]) {
        cout << 0 << "\n";
        return 0;
    }

    // 收集路径上所有方点包含的圆点
    vector<bool> used(N, false);
    ll ans = 0;
    int cur = T;
    while (true) {
        if (cur >= N) {
            int idx = cur - N;
            for (int x : members[idx]) {
                if (!used[x]) {
                    used[x] = true;
                    ans += val[x];
                }
            }
        }
        if (cur == S) break;
        cur = parent[cur];
    }

    cout << ans << "\n";
    return 0;
}