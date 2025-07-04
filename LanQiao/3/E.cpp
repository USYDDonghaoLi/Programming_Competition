#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>

using namespace std;

bool check(const vector<int>& nums, long long mid, int m) {
    long long cnt = 0, s = 0, s2 = 0;
    int idx = 0, n = nums.size();

    while (idx < n) {
        s += nums[idx];
        s2 += (long long)nums[idx] * nums[idx];
        if ((s * s - s2) / 2 > mid) {
            cnt++;
            s = 0;
            s2 = 0;
        } else {
            idx++;
        }
    }

    return cnt + 1 > m;
}

void solve() {
    int n, m;
    cin >> n >> m;
    vector<int> nums(n);
    for (int& num : nums) {
        cin >> num;
    }

    if (m >= n) {
        cout << (long long)*max_element(nums.begin(), nums.end()) * *max_element(nums.begin(), nums.end()) << endl;
        return;
    }

    long long l = 1, r = 1;
    for (int num : nums) {
        r += (long long)num * num;
    }

    while (l < r) {
        long long mid = l + (r - l) / 2;
        if (check(nums, mid, m)) {
            l = mid + 1;
        } else {
            r = mid;
        }
    }

    cout << l << endl;
}

int main() {
    int t = 1; // Assuming there's only one test case as in your Python code
    while (t--) {
        solve();
    }
    return 0;
}
