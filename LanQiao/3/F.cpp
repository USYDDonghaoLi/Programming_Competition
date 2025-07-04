#include <iostream>

using namespace std;

void solve() {
    long long n, k;
    cin >> n >> k;

    if ((n + 1) * n / 2 >= k) {
        long long l = 2, r = n + 1;
        while (l < r) {
            long long mid = l + (r - l) / 2;
            if (mid * (mid - 1) / 2 < k) {
                l = mid + 1;
            } else {
                r = mid;
            }
        }

        k -= (l - 1) * (l - 2) / 2;
        cout << k << " " << l - k << endl;
    } else {
        k = n * n + 1 - k;
        long long l = 2, r = n + 1;
        while (l < r) {
            long long mid = l + (r - l) / 2;
            if (mid * (mid - 1) / 2 < k) {
                l = mid + 1;
            } else {
                r = mid;
            }
        }

        k -= (l - 1) * (l - 2) / 2;
        cout << n + 1 - k << " " << n + 1 - (l - k) << endl;
    }
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}
