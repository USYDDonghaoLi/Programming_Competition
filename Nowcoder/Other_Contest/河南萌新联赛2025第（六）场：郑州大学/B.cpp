#include <iostream>
#include <vector>
#include <queue>
#include <climits>
#include <cassert>
#include <array>
#include <iomanip>

using namespace std;

const int N = 2000010;
vector<int> e[N];
int d[N], ans[N], st[N];
int tp;

void dfs(int u)
{
    st[++tp] = u;
    ++ans[u];
    --ans[st[tp - min(d[u] + 1, tp)]];
    for (int v : e[u])
    {
        e[v].erase(remove(e[v].begin(), e[v].end(), u), e[v].end());
        dfs(v);
        ans[u] += ans[v];
    }
    --tp;
}
int main()
{
    ios::sync_with_stdio(0); cin.tie(0);
    cout << fixed << setprecision(15);
    int n, i;
    cin >> n;
    for (i = 1; i < n; i++)
    {
        int u, v;
        cin >> u >> v;
        e[u].push_back(v);
        e[v].push_back(u);
    }
    for (i = 1; i <= n; i++) cin >> d[i];
    dfs(1);
    for (i = 1; i <= n; i++) cout << ans[i] << " \n"[i == n];
}