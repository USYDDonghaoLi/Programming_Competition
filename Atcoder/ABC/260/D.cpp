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
#define min(x, y) ((x) > (y) ? (y) : (x))
#define max(x, y) ((x) < (y) ? (x) : (y))
#define lowbit(x) ((x) & (-x))
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

const int N = 200010;
int n, k;

void solve(){
    scanf("%d%d", &n, &k);

    VI under(n + 5, -1);
    VI pile(n + 5, 0);
    set<int> st;
    VI res(n + 5, -1);

    rep(i, 1, n + 1){
        int p;
        scanf("%d", &p);
        auto it = st.upper_bound(p);
        if (it == st.end()){
            pile[p] = 1;
            st.insert(p);
        }
        else{
            under[p] = *it;
            pile[p] = pile[(*it)] + 1;
            st.erase(it);
            st.insert(p);
        }
        if (pile[p] == k){
            st.erase(p);
            int x = p;
            rep(j, 0, k){
                res[x] = i;
                x = under[x];
            }
        }
    }
    rep(i, 1, n + 1) printf("%d\n", res[i]);
}

int main(){
    int T;
    //scanf("%d", &T);
    T = 1;
    while (T--) solve();
    return 0;
}