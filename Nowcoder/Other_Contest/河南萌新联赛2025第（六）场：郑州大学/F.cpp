#include <iostream>
#include <vector>
#include <queue>
#include <string>
#include <climits>

using namespace std;

const int INF = 1e9;
const vector<pair<int, int>> d = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

void solve() {
    int n, m, k;
    cin >> n >> m >> k;
    vector<string> A(n);
    for (int i = 0; i < n; ++i) {
        cin >> A[i];
    }

    vector<vector<vector<int>>> dist(k + 1, vector<vector<int>>(n, vector<int>(m, INF)));
    dist[0][0][0] = 0;

    priority_queue<tuple<int, int, int, int>, vector<tuple<int, int, int, int>>, greater<>> pq;
    pq.emplace(0, 0, 0, 0);

    while (!pq.empty()) {
        auto [cost, x, y, used] = pq.top();
        pq.pop();
        if (dist[used][x][y] != cost) {
            continue;
        }
        for (const auto& [dx, dy] : d) {
            int nx = x + dx, ny = y + dy;
            if (nx >= 0 && nx < n && ny >= 0 && ny < m) {
                if (A[nx][ny] == '.') {
                    if (dist[used][nx][ny] > cost + 1) {
                        dist[used][nx][ny] = cost + 1;
                        pq.emplace(cost + 1, nx, ny, used);
                    }
                } else {
                    if (used < k && dist[used + 1][nx][ny] > cost + 1) {
                        dist[used + 1][nx][ny] = cost + 1;
                        pq.emplace(cost + 1, nx, ny, used + 1);
                    }
                }
            }
        }
    }

    int res = INF;
    for (int i = 0; i <= k; ++i) {
        res = min(res, dist[i][n - 1][m - 1]);
    }

    cout << (res == INF ? -1 : res) << "\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}