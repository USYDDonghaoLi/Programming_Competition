#include <iostream>
#include <vector>
#include <algorithm>
#include <limits>
#include <numeric> // For std::gcd

using namespace std;

int main() {
    int n, m, q;
    cin >> n >> m >> q;

    vector<vector<int>> grid(n, vector<int>(m));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            cin >> grid[i][j];
        }
    }

    vector<vector<vector<long long>>> dp(n, vector<vector<long long>>(m, vector<long long>(q + 1, numeric_limits<long long>::min())));
    dp[0][0][0] = grid[0][0];

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            if (i > 0) {
                int g = gcd(grid[i][j], grid[i - 1][j]);
                for (int k = g == 1 ? 1 : 0; k <= q; ++k) {
                    dp[i][j][k] = max(dp[i][j][k], dp[i - 1][j][k - (g == 1)] + grid[i][j]);
                }
            }
            if (j > 0) {
                int g = gcd(grid[i][j], grid[i][j - 1]);
                for (int k = g == 1 ? 1 : 0; k <= q; ++k) {
                    dp[i][j][k] = max(dp[i][j][k], dp[i][j - 1][k - (g == 1)] + grid[i][j]);
                }
            }
        }
    }

    long long res = *max_element(dp[n - 1][m - 1].begin(), dp[n - 1][m - 1].end());
    if (res <= 0LL) {
        cout << -1 << endl;
    } else {
        cout << res << endl;
    }

    return 0;
}
