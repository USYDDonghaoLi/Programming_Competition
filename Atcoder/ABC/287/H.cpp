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
const int N = 2010;

int dir[4][2] = {1, 0, -1, 0, 0, -1, 0, 1};
vector<int> adj[N];


bool check(int s, int t, int mid, int n){
    queue<int> q;
    vector<int> v(n + 1);
    q.push(s);

    while (!q.empty()){
        int cur = q.front();
        if (cur == t) return true;
        q.pop();
        for (int o: adj[cur]){
            if (o <= mid && !v[o]){
                v[o] = 1;
                q.push(o);
            }
        }
    }
    return false;
}

void solve(int testcase){
    int n, m;
    cin >> n >> m;
    for (int i = 0; i < m; i++){
        int a, b;
        cin >> a >> b;
        adj[a].emplace_back(b);
    }

    int q;
    cin >> q;
    for (int i = 0; i < q; i++){
        int s, t;
        cin >> s >> t;

        int l = max(s, t), r = n + 1;
        for(; l < r; ){
            int mid = l + r >> 1;
            if (check(s, t, mid, n)){
                r = mid;
            }
            else{
                l = mid + 1;
            }
        }

        if (l == n + 1){
            cout << -1 << "\n";
        }
        else{
            cout << l << "\n";
        }
    }
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0); cout.tie(0);
    int T = 1;
    //cin >> T;
    for (int testcase = 1; testcase <= T; testcase++) solve(testcase);
    return 0;
}