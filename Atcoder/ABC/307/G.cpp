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

int dir[4][2] = {1, 0, -1, 0, 0, -1, 0, 1};

void solve(int testcase){
    int n;
    cin >> n;

    vector<long long> A(n, 0LL), B(n + 1, 0LL);
    for (int i = 0; i < n; i++){
        cin >> A[i];
        B[i + 1] = B[i] + A[i];
    }

    long long a, b;
    a = B[n] / n;
    if (B[n] % n != 0 && B[n] < 0){
        a--;
    }
    b = B[n] - a * n;

    vector<vector<long long>> dp(n + 1, vector<long long>(b + 1, infl));
    dp[0][0] = 0;

    for (int i = 0; i < n; i++){
        for (int j = 0; j < b + 1; j++){
            long long change = B[i + 1] - (i * a + j);
            for (int k = 0; k < 2; k++){
                if (j + k < b + 1){
                    chmin(dp[i + 1][j + k], dp[i][j] + abs(a + k - change));
                }
            }
        }
    }

    cout << dp[n][b] << "\n";

}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0); cout.tie(0);
    int T = 1;
    // cin >> T;
    for (int testcase = 1; testcase <= T; testcase++) solve(testcase);
    return 0;
}