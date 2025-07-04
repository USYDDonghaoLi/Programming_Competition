#include <bits/stdc++.h>
using namespace std;

#define rep(i, a, n) for(int i = a; i < n; i++)
#define pre(i, a, n) for(int i = n - 1; i >= a; i--)
#define pb push_back
#define eb emplace_back
#define mp make_pair
#define all(x) (x).begin(),(x).end()
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

void solve(){
    string s;
    map<char, int> cnt;
    cin >> s;
    for (auto p: s) cnt[p]++;
    for (auto [p, q]: cnt) if (q == 1){
        cout << p;
        return;
    }
    cout << -1;
}

int main(){
    int T;
    //scanf("%d", &T);
    T = 1;
    while (T--) solve();
    return 0;
}