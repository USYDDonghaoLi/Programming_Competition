#pragma GCC optimize(1)
#pragma GCC optimize(2)
#pragma GCC optimize(3,"Ofast","inline")
#include<bits/stdc++.h>
using namespace std;

const long long mod = 1000000007;

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

const int maxcnt = 15000010;
const int Size = 2;
struct Trie {
    int root, cnt;
    int tree[maxcnt][Size];
    int sz[maxcnt];
    int create() {
        ++cnt;
        memset(tree[cnt], 0, sizeof(tree[cnt]));
        sz[cnt] = 0;
        return cnt;
    }
    void Init() {
        cnt = 0;
        root = create();
    }

    void add(int num){
        int pos = root;
        sz[pos]++;
        for (int i = 30; i >= 0; i--){
            int w = num >> i & 1;
            if (tree[pos][w] == 0){
                tree[pos][w] = create();
            }
            pos = tree[pos][w];
            sz[pos]++;
        }
    }

    void del(int num){
        int pos = root;
        sz[pos]--;
        for (int i = 30; i >= 0; i--){
            int w = num >> i & 1;
            if (tree[pos][w] == 0){
                tree[pos][w] = create();
            }
            pos = tree[pos][w];
            sz[pos]--;
        }
    }
    long long query(int num){
        int pos = root;
        long long res = 0;
        for (int i = 30; i >= 0; i--){
            int w = num >> i & 1;
            if (tree[pos][1 - w] && sz[tree[pos][1 - w]]){
                res |= 1 << i;
                pos = tree[pos][1 - w];
            }
            else if (tree[pos][w] && sz[tree[pos][w]]){
                pos = tree[pos][w];
            }
            else{
                break;
            }
        }
        return res;
    }
};

Trie T;

const int N = 500010;
vector<int> adj[N], child[N];
long long prob[N], vals[N], A[N];
long long res;

void dfs(int node, int parent){
    for (auto& o: adj[node]){
        if (o == parent) continue;
        child[node].push_back(o);
        vals[o] = vals[node] ^ A[o];
        dfs(o, node);
    }
}

void dfs2(int node){
    if (node == 1){
        T.Init();
    }
    T.add(A[node]);
    int t = child[node].size();
    if (t){
        for (auto& o: child[node]){
            prob[o] = prob[node] * quickpow(t, mod - 2, mod) % mod;
            dfs2(o);
        }
    }
    else{
        res += prob[node] * T.query(vals[node]) % mod;
        res %= mod;
    }
    T.del(A[node]);
}

void solve(int testcase){
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++){
        adj[i].clear();
        child[i].clear();
        cin >> A[i];
    }

    for (int i = 1; i < n; i++){
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    vals[1] = A[1];
    dfs(1, 0);

    prob[1] = 1LL;
    res = 0LL;
    dfs2(1);

    cout << res << "\n";
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0); cout.tie(0);
    int T = 1;
    cin >> T;
    for (int testcase = 1; testcase <= T; testcase++) solve(testcase);
    return 0;
}