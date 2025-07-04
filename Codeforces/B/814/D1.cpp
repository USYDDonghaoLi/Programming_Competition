

#include <bits/stdc++.h>
using namespace std;

const int N = 9000;
int n, nums[N];
float dp[N], temp[N];

void solve(){
    std::cin >> n;
    for (int i = 0; i < n; ++i) std::cin >> nums[i];
    std::memset(dp, 10000, sizeof(dp));
    dp[nums[0]] = nums[0] == 0 ? 0 : 0.5;

    for (int i = 1; i < n; ++i){
        std::memset(temp, 10000, sizeof(temp));
        int m = 10000;
        for (int j = 0, j < N; ++j) m = std::min(std::ceil(dp[j]), m);

        if (nums[i]) temp[nums[i]] = std::min(temp(nums[i]), m + 0.5);
        else {
            temp[0] = m;
            continue;
        }

        for (int j = 0; j < M; ++j){
            if (dp[j] != 10000){
                if (nums[i] ^ j == 0) temp[j] = std::min(temp[j], dp[j] + 0.5);
                else temp[nums[i] ^ j] = std::min(temp[nums[i] ^ j], std::ceil(dp[j]) + 0.5);
            }
        }

        for (int j = 0; j < M; ++j) dp[j] = temp[j];
    }

    int res = 10000;
    for (j = 0; j < M; ++j) res = std::min(res, std::ceil(dp[j]));
    std::cout << res;
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0);
    int T = 1;
    cin >> T;
    for (;T--;) solve();
    return 0;
}