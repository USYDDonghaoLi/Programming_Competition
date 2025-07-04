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

const int N = 3010, M = 3010;
int dp[N][M][2], ans[M], nums[N];

void solve(int testcase){

    int n, m;
    cin >> n >> m;
    for (int i = 0; i < n; i++){
        cin >> nums[i];
    }
 
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m + 1; j++)
            for (int k = 0; k < 2; k++)
                dp[i][j][k] = 0x3f3f3f3f;
    
    memset(ans, 0x3f3f3f3f, sizeof(ans));
 
    dp[0][nums[0]][0] = 0;
    dp[0][0][1] = 1;
    ans[0] = 1;
    if (n == 1) ans[nums[0]] = 0;
    else ans[nums[0]] = 1;
 
    for (int i = 0; i < n - 1; i++){
        for (int j = 0; j < m + 1; j++){
            if (j + nums[i + 1] <= m){
                dp[i + 1][j + nums[i + 1]][0] = min(dp[i + 1][j + nums[i + 1]][0], min(dp[i][j][0], dp[i][j][1]));
                ans[j + nums[i + 1]] = min(ans[j + nums[i + 1]], dp[i + 1][j + nums[i + 1]][0] + (int)(i != n - 2));
            }
            dp[i + 1][j][1] = min(dp[i + 1][j][1], min(dp[i][j][1], dp[i][j][0] + 1));
            ans[j] = min(ans[j], dp[i + 1][j][1]);
        }
    }
 
    for (int i = 1; i < m + 1; i++){
        if (ans[i] >= 0x3f3f3f3f) cout << -1 << "\n";
        else cout << ans[i] << "\n";
    }
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0); cout.tie(0);
    int T = 1;
    //cin >> T;
    for (int testcase = 1; testcase <= T; testcase++) solve(testcase);
    return 0;
}