#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <bitset>
#include <cassert>

using namespace std;

// Direction deltas
int d[8][2] = {{-1, 0}, {1, 0}, {0, 1}, {0, -1}, {1, 1}, {1, -1}, {-1, 1}, {-1, -1}};

void solve() {
    int n, m;
    cin >> n >> m;
    vector<string> grid(n);
    for (int i = 0; i < n; ++i) {
        cin >> grid[i];
    }

    vector<pair<int, int>> coordinates;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            if (!isdigit(grid[i][j])) {
                coordinates.push_back({i, j});
            }
        }
    }

    int k = coordinates.size();
    assert (k <= 16);
    bool flag = false;

    vector<vector<char>> tmp(n, vector<char>(m));
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                tmp[i][j] = grid[i][j];
            }
        }

    auto check = [&](int state) {

        for (int bit = 0; bit < k; ++bit) {
            auto& [x, y] = coordinates[bit];
            tmp[x][y] = (state & (1 << bit)) ? 'X' : '.';
        }

        for (int x = 0; x < n; ++x) {
            for (int y = 0; y < m; ++y) {
                if (isdigit(grid[x][y])) {
                    int cnt = 0, num = grid[x][y] - '0';
                    for (auto& [dx, dy] : d) {
                        int nx = x + dx, ny = y + dy;
                        if (0 <= nx && nx < n && 0 <= ny && ny < m && tmp[nx][ny] == 'X') {
                            cnt++;
                        }
                    }
                    if (cnt != num) {
                        return false;
                    }
                }
            }
        }
        return true;
    };

    for (int i = 0; i < (1 << k); ++i) {
        if (check(i)) {
            if (flag) {
                cout << "Multiple" << "\n";
                return;
            } else {
                flag = true;
            }
        }
    }

    cout << (flag ? "Single" : "Impossible") << "\n";
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);

    int t;
    cin >> t;
    while (t--) {
        solve();
    }

    return 0;
}
