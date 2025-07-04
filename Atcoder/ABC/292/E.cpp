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
const int N = 2010;
int adj[N][N];

void solve(int testcase){
    int n, m;
    cin >> n >> m;
    for (int i = 0; i < m; i++){
        int u, v;
        cin >> u >> v;
        adj[u][v] = 1;
    }

    long long res = 0;
    for (int i = 1; i <= n; i++){
        queue<int> q;
        q.push(i);
        vector<int> f(n + 1, 0);
        f[i] = 1;

        while (!q.empty()){
            int cur = q.front();
            q.pop();
            for (int j = 1; j <= n; j++){
                if (f[j] || (!adj[cur][j])){
                    continue;
                }
                else{
                    q.push(j);
                    f[j] = 1;
                    if (!adj[i][j]){
                        ++res;
                    }
                }
            }
        }
    }   

    cout << res << "\n";
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0); cout.tie(0);
    int T = 1;
    // cin >> T;
    for (int testcase = 1; testcase <= T; testcase++) solve(testcase);
    return 0;
}