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

const int mod = 1000000007;
int dir[4][2] = {1, 0, -1, 0, 0, -1, 0, 1};
int f[22][1 << 21], a[21];
int n;

int dfs(int idx, int state){
    if (f[idx][state] != -1){
        return f[idx][state];
    }

    int ret = 0;
    for (int i = 0; i < n; i++){
        if ((a[idx] >> i & 1) && !(state >> i & 1)){
            int newstate = state | (1 << i);
            ret += dfs(idx + 1, newstate);
            ret %= mod;
        }
    }
    return f[idx][state] = ret;
}

void solve(int testcase){
    memset(f, -1, sizeof(f));
    memset(a, 0, sizeof(a));
    cin >> n;
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            int k;
            cin >> k;
            if (k){
                a[i] |= 1 << j;
            }
        }
    }

    for (int j = 0; j < (1 << n) - 1; j++){
        f[n][j] = 0;
    }
    f[n][(1 << n) - 1] = 1;

    dfs(0, 0);
    // for (int i = 0; i <= n; i++){
    //     for (int j = 0; j < (1 << n); j++){
    //         cout << f[i][j] << " \n"[j == (1 << n) - 1];
    //     }
    // }

    cout << f[0][0] << "\n";
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0); cout.tie(0);
    int T = 1;
    //cin >> T;
    for (int testcase = 1; testcase <= T; testcase++) solve(testcase);
    return 0;
}