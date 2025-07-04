#include <bits/stdc++.h>
using namespace std;

#define rep(i, a, n) for(int i = a; i < n; i++)
#define per(i, a, n) for(int i = n - 1; i >= a; i--)
#define pb push_back
#define eb emplace_back
#define mp make_pair
#define all(x) (x).begin(), (x).end()
#define rall(x) (x).rbegin(), (x).rend()
#define rev(x) reverse(all(x))
#define srt(x) sort(all(x))
#define rsrt(x) sort(rall(x))
#define fi first
#define se second
#define SZ(x) ((int)(x).size())
typedef vector<int> VI;
typedef basic_string<int> BI;
typedef long long ll;
typedef pair<int, int> PII;
typedef double db;
mt19937 mrand(random_device{}());
const ll mod = 1000000007;
int rnd(int x){ return mrand() % x;}
ll powmod(ll a, ll b){
    ll res = 1;
    a %= mod;
    assert(b >= 0);
    for (; b ; b >>= 1){
        if (b & 1){
            res *= a;
            res %= mod;
        }
        a *= a;
        a %= mod;
    }
    return res;
}
ll gcd(ll a, ll b){
    return b ? gcd(b, a % b) : a;
}

const int N = 100010;
vector<vector<int>> f(N);

int ops(vector<int> arr){
    int even = 0, odd = 0, m = arr.size();
    rep(i, 0, m){
        if (arr[i] & 1) {odd = max(even + 1, odd);}
        else {even = max(even, odd + 1);}
    }
    return max(even, odd);
}

void solve(){
    int n;
    scanf("%d", &n);
    rep(i, 1, n + 1) f[i].clear();
    rep(i, 1, n + 1){
        int v;
        scanf("%d", &v);
        f[v].eb(i);
    }
    vector<int> g(n + 1, 0);
    rep(i, 1, n + 1) if (!f[i].empty()) {g[i] = ops(f[i]);}
    rep(i, 1, n + 1){printf("%d ", g[i]);}
    printf("\n");
}

int main(){
    int T;
    scanf("%d", &T);
    //T = 1;
    while (T--) solve();
    return 0;
}