#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

#define int long long
const int inf = LLONG_MIN;

const int dx[] = {0, 1, 0, -1, 0};
const int dy[] = {1, 0, -1, 0, 0};

void solve() {
    int n, m, k;
    cin >> n >> m >> k;
    int sx, sy;
    cin >> sx >> sy;
    sx--; sy--;

    vector<vector<int>> grid(n, vector<int>(m));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            cin >> grid[i][j];
        }
    }

    vector<vector<int>> dp(n, vector<int>(m, inf));
    dp[sx][sy] = 0;
    int res = k * grid[sx][sy];

    for (int step = 1; step <= min(k, n * m); ++step) {
        vector<vector<int>> newdp(n, vector<int>(m, inf));
        for (int x = 0; x < n; ++x) {
            for (int y = 0; y < m; ++y) {
                for (int dir = 0; dir < 5; ++dir) {
                    int nx = x + dx[dir];
                    int ny = y + dy[dir];
                    if (nx >= 0 && nx < n && ny >= 0 && ny < m) {
                        newdp[nx][ny] = max(newdp[nx][ny], dp[x][y] + grid[nx][ny]);
                    }
                }
            }
        }
        dp = newdp;
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                res = max(res, dp[i][j] + (k - step) * grid[i][j]);
            }
        }
    }

    cout << res << endl;
}

int32_t main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    int t = 1;
    // cin >> t; // Uncomment if there are multiple test cases
    while (t--) {
        solve();
    }
    return 0;
}
