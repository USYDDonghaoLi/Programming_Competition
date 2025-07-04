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

const int N = 200010;
int dir[4][2] = {1, 0, -1, 0, 0, -1, 0, 1};
int s[512], mp[262144];

void init(){
    for(int i = 0; i < 512; i++){
        s[i] = i * i;
    }
}

void solve(int testcase){
    int n;
    cin >> n;
    memset(mp, 0, sizeof(mp));
    mp[0] = 1;

    long long res = 0;
    int cur = 0;
    for (long long i = 0; i < n; i++){
        int a;
        cin >> a;
        res += i + 1;
        cur ^= a;
        for (int j = 0; j < 512; j++){
            int t = cur ^ (s[j]);
            // if (mp.find(t) != mp.end()){
            //     res -= mp[t];
            // }
            res -= mp[t];
        }
        mp[cur] += 1;
    }

    cout << res << "\n";
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0); cout.tie(0);
    init();
    int T = 1;
    cin >> T;
    for (int testcase = 1; testcase <= T; testcase++) solve(testcase);
    return 0;
}