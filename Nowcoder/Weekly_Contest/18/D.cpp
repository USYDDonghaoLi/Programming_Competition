#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

#define INF LLONG_MIN

long long dp[1010][1010][3];

void solve(int testcase) {
    int n, x;
    cin >> n >> x;
    vector<int> A(n), B(n);
    for (int i = 0; i < n; ++i) cin >> A[i];
    for (int i = 0; i < n; ++i) cin >> B[i];

    for (int i = 0; i <= n; ++i)
        for (int j = 0; j <= x; ++j)
            for (int k = 0; k < 3; ++k)
                dp[i][j][k] = INF;

    dp[0][0][0] = 0;

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j <= x; ++j) {
            for (int k = 0; k < 3; ++k) {
                if (k == 0) {
                    // Full price / Don't buy
                    dp[i + 1][j][0] = max(dp[i + 1][j][0], dp[i][j][k]);
                    if (j + A[i] <= x)
                        dp[i + 1][j + A[i]][1] = max(dp[i + 1][j + A[i]][1], dp[i][j][k] + B[i]);
                } else if (k == 1) {
                    // Full price / Half price / Don't buy
                    dp[i + 1][j][0] = max(dp[i + 1][j][0], dp[i][j][k]);
                    if (j + A[i] <= x)
                        dp[i + 1][j + A[i]][1] = max(dp[i + 1][j + A[i]][1], dp[i][j][k] + B[i]);
                    if (j + A[i] / 2 <= x)
                        dp[i + 1][j + A[i] / 2][2] = max(dp[i + 1][j + A[i] / 2][2], dp[i][j][k] + B[i]);
                } else {
                    // Full price / Don't buy
                    dp[i + 1][j][0] = max(dp[i + 1][j][0], dp[i][j][k]);
                    if (j + A[i] <= x)
                        dp[i + 1][j + A[i]][1] = max(dp[i + 1][j + A[i]][1], dp[i][j][k] + B[i]);
                }
            }
        }
    }

    long long res = 0;
    for (int i = 0; i <= n; ++i)
        for (int j = 0; j <= x; ++j)
            for (int k = 0; k < 3; ++k)
                res = max(res, dp[i][j][k]);

    cout << res << endl;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int testcase = 1;
    // Uncomment if there's more than one test case
    // cin >> testcase;
    while (testcase--) {
        solve(testcase);
    }

    return 0;
}
