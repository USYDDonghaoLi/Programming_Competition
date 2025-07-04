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

ll max(ll a, ll b){
    return a > b ? a : b;
}

ll min(ll a, ll b){
    return a < b ? a : b;
}

const int N = 100010;
ll h[N], n;
void solve(){
    scanf("%d", &n);
    rep(i, 1, n + 1) {scanf("%lld", h + i);}
    if (n & 1){
        ll res = 0;
        for (int i = 2; i <= n - 1; i += 2) res += max(0, max(h[i - 1], h[i + 1]) + 1 - h[i]);
        printf("%lld\n", res);
    }
    else{
        ll res = 0;
        for (int i = 2; i <= n - 2; i += 2) res += max(0, max(h[i - 1], h[i + 1]) + 1 - h[i]);
        //printf("res is %lld\n", res);
        ll temp = res;
        for (int i = n - 2; i >= 2; i -= 2) {
            temp -= max(0, max(h[i - 1], h[i + 1]) + 1 - h[i]);
            temp += max(0, max(h[i], h[i + 2]) + 1 - h[i + 1]);
            //printf("temp is %lld\n", temp);
            res = min(res, temp);
            //printf("res is %lld\n", res);
        }
        printf("%lld\n", res);
    }   
}

int main(){
    int T;
    scanf("%d", &T);
    //T = 1;
    while (T--) solve();
    return 0;
}