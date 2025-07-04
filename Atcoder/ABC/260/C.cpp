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

ll dp[15][2], n, x, y;

void solve(){
    scanf("%d%d%d", &n, &x, &y);
    dp[n][0] = 1;
    dp[n][1] = 0;
    per(i, 2, n + 1){
        dp[i - 1][0] += dp[i][0];
        dp[i][1] += 1LL * x * dp[i][0];
        dp[i - 1][0] += dp[i][1];
        dp[i - 1][1] += 1LL * y * dp[i][1];
        //printf("%lld %lld %lld\n", i, dp[i][0], dp[i][1]);
    }
    printf("%lld", dp[1][1]);
}

int main(){
    int T;
    //scanf("%d", &T);
    T = 1;
    while (T--) solve();
    return 0;
}