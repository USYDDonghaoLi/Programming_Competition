#include <iostream>
#include <vector>
#include <chrono>
#include <random>
#include <cassert>
 
std::mt19937 rng((int) std::chrono::steady_clock::now().time_since_epoch().count());
 
int main() {
    std::ios_base::sync_with_stdio(false); std::cin.tie(NULL);
    int n;
    std::cin >> n;
    std::vector<int> a(n);
    for(int i = 0; i < n; i++) {
        std::cin >> a[i];
    }
    std::vector<long long> dp(n, 1e18);
    dp[0] = 0;
    for(int i = 0; i < n; i++) {
        int dist = n / a[i] + 1;
        // take from behind
        for(int j = i-1; j >= 0 && i-j <= dist; j--) {
            dp[i] = std::min(dp[i], dp[j] + (long long) a[i] * (i - j) * (i - j));
            if(a[j] <= a[i]) break;
        }
        // propagate forward
        for(int j = i+1; j < n && j-i <= dist; j++) {
            dp[j] = std::min(dp[j], dp[i] + (long long) a[i] * (i - j) * (i - j));
            if(a[j] <= a[i]) break;
        }
        std::cout << dp[i] << (i + 1 == n ? '\n' : ' ');
    }
}