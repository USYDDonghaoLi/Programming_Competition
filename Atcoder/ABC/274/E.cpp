#pragma GCC optimize(1)
#pragma GCC optimize(2)
#pragma GCC optimize(3,"Ofast","inline")
#include<bits/stdc++.h>
using namespace std;

template <class T>
void chmin(T &a, T b){
    if (b < a) a = b;
}
template <class T>
void chmax(T &a, T b){
    if (b > a) a = b;
}

constexpr int N = 17;
constexpr double INF = 9e18;
double dp[1 << N][N];
double x[N + 1], y[N + 1];
double dis[N + 1][N];

void solve(){
    int n, m;
    cin >> n >> m;
    for (int i = 0; i < n + m; i++){
        cin >> x[i] >> y[i];
    }

    x[n + m] = y[n + m] = 0;
    //calculate distance between places
    for (int i = 0; i <= n + m; i++){
        for (int j = 0; j < n + m; j++){
            double dx = x[i] - x[j];
            double dy = y[i] - y[j];
            dis[i][j] = sqrt(dx * dx + dy * dy);
        }
    }

    //initialize dp
    for (int i = 0; i < 1 << (n + m); i++){
        for (int j = 0; j < (n + m); j++){
            dp[i][j] = INF;
        }
    }
    for (int i = 0; i < n + m; i++){
        dp[1 << i][i] = dis[n + m][i];
    }

    //updating results of each state
    int mask = ((1 << m) - 1) << n;
    for (int k = 0; k < (1 << (n + m)); k++){
        for (int i = 0; i < n + m; i++){
            if (k & 1 << i){
                double t = dp[k][i];
                int l = k ^ (1 << i);
                int c = __builtin_popcount(l & mask);
                double speed = 1;
                while (c--){
                    speed *= 0.5;
                }
                for (int j = 0; j < n + m; j++){
                    chmin(t, dp[l][j] + dis[i][j] * speed);
                }
                dp[k][i] = t;
            }
        }
    }

    double res = INF;
    for (int k = 0; k < 1 << (n + m); k++){
        if (~k & (1 << n) - 1) continue;
        int c = __builtin_popcount(k & mask);
        double speed = 1;
        while (c--) speed *= 0.5;
        for (int i = 0; i < m + n; i++){
            chmin(res, dp[k][i] + dis[m + n][i] * speed);
        }
    }
    cout << fixed << setprecision(10);
    cout << res << "\n";
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0);
    int T = 1;
    //cin >> T;
    for (;T--;) solve();
    return 0;
}