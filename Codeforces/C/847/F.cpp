#include <bits/stdc++.h>

using namespace std;


class lca{
public:
    int n;
    int m;
    int * depth;
    int ** fa;
    map<int, vector<int>> graph;
    vector<int> ancestor(n + 1);
    
    lca(){}
    lca(int n_){
        n = n_;
        m = (int)((double)log(n) / log(2));
        depth = new int[n];
        fa = new int * [n];
        for (int i = 0; i < n; i ++){
            depth[i] = INT_MAX;
            fa[i] = new int [m];
            for (int j = 0; j < m; j ++){
                fa[i][j] = -1;
            }
        }
    }
    
    void addedge(int a, int b){
        graph[a].push_back(b);
        graph[b].push_back(a);
    }
    
    void bfs(int root){
        depth[root] = 0;
        queue<int> q;
        q.push(root);
        // cout << root << ' ' << n << ' ' << m << endl;
        for (int k = 0; k < m; k ++){
            fa[root][k] = root;
        }
        while (!q.empty()){
            int curLen = (int)q.size();
            for (int _ = 0; _ < curLen; _ ++){
                int cur = q.front(); q.pop();
                for (int e: graph[cur]){
                    if (depth[e] > depth[cur] + 1){
                        depth[e] = depth[cur] + 1;
                        q.push(e);
                        fa[e][0] = cur;
                        for (int i = 1; i < m; i ++){
                            fa[e][i] = fa[fa[e][i - 1]][i - 1];
                        }
                    }
                    if (depth[e] == 1){
                        ancestor[e] = e;
                    }
                    else{
                        ancestor[e] = ancestor[cur];
                    }
                }
            }
        }
    }
    
    int sol(int a, int b){
        if (depth[a] < depth[b]){
            swap(a, b);
        }
        
        for (int k = m - 1; k > -1; k --){
            if (depth[fa[a][k]] >= depth[b]){
                a = fa[a][k];
            }
        }
        
        if (a == b){
            return a;
        }
        for (int k = m - 1; k > -1; k --){
            if (fa[a][k] != fa[b][k]){
                a = fa[a][k];
                b = fa[b][k];
            }
        }
        
        return fa[a][0];
    }
    
    // int routes(int a, int b){
        
    // }
    
};




void solve(){
    int n, c;
    cin >> n >> c;
    int state[n + 1];
    memset(state, 0, sizeof(state));
    vector<int> visited(n + 1);
    state[c] = 1;
    int now = n;
    vector<int> res;
    
    int ops[n + 1];
    ops[0] = c;
    for (int i = 1; i < n; i ++){
        cin >> ops[i];
    }
    
    map<int, vector<int>> adj;
    lca LCA = lca(n + 1);
    for (int i = 0; i < n - 1; i ++){
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
        LCA.addedge(u, v);
    }
    
    LCA.bfs(c);
    
    int i = 1; 
    while (i < n){
        state[ops[i]] = 1;
        if (!visited[LCA.ancestor[ops[i]]]){
            now = min(now, LCA.depth[ops[i]])
            visited[LCA.ancestor[ops[i]]] = true;
        }
        else{
            for (int j = 0; j < i ; j ++){
                int ancestor = LCA.sol(ops[i], ops[j]);
                now = min(now, LCA.depth[ops[i]] + LCA.depth[ops[j]] - 2 * LCA.depth[ancestor]);
            }
        }
        res.push_back(now);
        if (now < 400){
            break;
        }
        i ++;
    }
    
    for (int j = i + 1; j < n; j ++){
        int node = ops[j];
        state[node] = 1;
        int step = 0;
        queue<pair<int, int>> q;
        q.push({node, 0});
        while (!q.empty()){
            int curLen = (int)q.size();
            for (int _ = 0; _ < curLen; _ ++){
                auto [cur, fa] = q.front();  q.pop();
                if (state[cur] > 0 && cur != node){
                    now = step;
                    break;
                }
                for (int o: adj[cur]){
                    if (o == fa){
                        continue;
                    }else{
                        q.push({o, cur});   
                    }
                }
            }
            step ++;
            if (step >= now){
                break;
            }
        }
        res.push_back(now);
    }
    
    // cout << res.size();
    for (int i = 0; i < (int)res.size(); i ++){
        cout << res[i];
        if (i < (int)res.size() - 1){
            cout << ' ';
        }
    }
    cout << endl;
    
}
    


int main(){
    std::ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    
    int T;
    cin >> T;
    while (T --){
        solve();
    }
    
    return 0;
}

