#include <bits/stdc++.h>
using namespace std;

#define rep(i, a, n) for(int i = a; i < n; i++)
#define pre(i, a, n) for(int i = n - 1; i >= a; i--)
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

const int N = 1010;
int n, x, y, z, a[N], b[N], vis[N];
void solve(){
    scanf("%d%d%d%d", &n, &x, &y, &z);
    rep(i, 0, n) scanf("%d", a + i);
    rep(i, 0, n) scanf("%d", b + i);
    rep(i, 0, x){
        PII ps(-1, -1);
        rep(i, 0, n) if(!vis[i]){
            ps = max(ps, mp(a[i], -i));
        }
        vis[-ps.se] = 1;
    }
    rep(i, 0, y){
        PII ps(-1, -1);
        rep(i, 0, n) if(!vis[i]){
            ps = max(ps, mp(b[i], -i));
        }
        vis[-ps.se] = 1;
    }
    rep(i, 0, z){
        PII ps(-1, -1);
        rep(i, 0, n) if(!vis[i]){
            ps = max(ps, mp(a[i] + b[i], -i));
        }
        vis[-ps.se] = 1;
    }
    rep(i, 0, N) if (vis[i]) printf("%d\n", i + 1);
}

int main(){
    int T;
    //scanf("%d", &T);
    T = 1;
    while (T--) solve();
    return 0;
}