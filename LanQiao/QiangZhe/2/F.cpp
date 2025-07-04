#include <iostream>
#include <vector>
using namespace std;

const int MOD = 998244353;

void solve(int testcase) {
    int n, m;
    cin >> n >> m;
    vector<int> nums(n, -1);
    for (int i = 0; i < m; ++i) {
        int a, b;
        cin >> a >> b;
        --a; --b;
        nums[a] = b;
    }

    vector<vector<long long>> dp(n, vector<long long>(72, 0));
    for (int i = 0; i < n; ++i) {
        int v = nums[i];
        if (i == 0) {
            if (v == -1) {
                for (int j = 0; j < 72; ++j) {
                    dp[i][j] = 1;
                }
            } else {
                dp[i][v] = 1;
            }
        } else {
            long long s = 0;
            for (int j = 0; j < 72; ++j) {
                s = (s + dp[i - 1][j]) % MOD;
            }
            if (v == -1) {
                for (int j = 0; j < 72; ++j) {
                    dp[i][j] = (s - dp[i - 1][j] + MOD) % MOD;
                }
            } else {
                dp[i][v] = (s - dp[i - 1][v] + MOD) % MOD;
            }
        }
    }

    long long sum = 0;
    for (int i = 0; i < 72; ++i) {
        sum = (sum + dp[n - 1][i]) % MOD;
    }
    cout << sum << endl;
}

int main() {
    int testcase = 1;
    // cin >> testcase; // 如果有多个测试用例可以取消注释
    while (testcase--) {
        solve(testcase);
    }
    return 0;
}
