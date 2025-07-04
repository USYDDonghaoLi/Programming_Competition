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

int idx2val[N], val2idx[N], P[N], f[N];
int dir[4][2] = {1, 0, -1, 0, 0, -1, 0, 1};

void solve(int testcase){
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++){
        cin >> P[i];
    }
    for (int i = 1; i <= n; i++){
        idx2val[i] = P[i];
        val2idx[P[i]] = i;
    }

    int idx = 0;
    int m = sqrt(n + n);
    for (int i = 1; i <= n; i++){
        int t = inf;
        int left = max(1, i - m);
        int right = min(i + m, n);
        int left2 = max(1, idx2val[i] - m);
        int right2 = min(idx2val[i] + m, n);

        for (int j = left; j <= right; j++){
            if (i == j) continue;
            else chmin(t, abs(i - j) + abs(idx2val[i] - idx2val[j]));
        }
        for (int j = left2; j <= right2; j++){
            if (idx2val[i] == j) continue;
            else chmin(t, abs(idx2val[i] - j) + abs(i - val2idx[j]));
        }
        f[idx++] = t;
    }

    for (int i = 0; i < n; i++){
        cout << f[i] << " \n"[i == n - 1];
    }
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0); cout.tie(0);
    int T = 1;
    //cin >> T;
    for (int testcase = 1; testcase <= T; testcase++) solve(testcase);
    return 0;
}