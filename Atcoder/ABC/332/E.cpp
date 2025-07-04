#include <iostream>
#include <vector>
#include <unordered_map>
#include <cmath>
#include <functional>
using namespace std;

// 快速输入输出
void fast_io() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

// 动态规划的记忆化搜索
unordered_map<int, unordered_map<int, long long>> dp;
long long calc(int step, int state, int n, int d, const vector<int>& nums) {
    if (step == d) {
        return (state == (1 << n) - 1) ? 0 : LLONG_MAX;
    }

    if (dp[step].find(state) != dp[step].end()) {
        return dp[step][state];
    }

    long long res = LLONG_MAX;
    for (int i = 1; i < (1 << n); ++i) {
        bool flag = true;
        for (int j = 0; j < n; ++j) {
            if ((state >> j) & 1 && (i >> j) & 1) {
                flag = false;
                break;
            }
        }
        if (!flag) continue;

        long long tmp = 0;
        for (int j = 0; j < n; ++j) {
            if (i >> j & 1) {
                tmp += nums[j];
            }
        }

        res = min(res, tmp * tmp + calc(step + 1, state | i, n, d, nums));
    }

    return dp[step][state] = res;
}

void solve() {
    int n, d;
    cin >> n >> d;
    vector<int> nums(n);
    long long s = 0;
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
        s += nums[i];
    }

    long long ans = (calc(0, 0, n, d, nums) - 2 * s / d * s + d * pow(s / d, 2)) / d;
    cout << ans << "\n";
}

int main() {
    fast_io();
    // 假设有一个测试用例
    solve();
    return 0;
}
