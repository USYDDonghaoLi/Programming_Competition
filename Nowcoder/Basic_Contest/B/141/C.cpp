#include <bits/stdc++.h>
using namespace std;

const long long inf = LLONG_MAX;

void solve(int testcase) {
    string s;
    long long x;
    cin >> s >> x;

    int n = s.length();
    vector<int> s_int(n);
    for (int i = 0; i < n; ++i) {
        s_int[i] = s[i] - 'a';
    }

    vector<vector<long long>> cnt(n + 1, vector<long long>(26, 0));
    vector<long long> A(n + 1, 0);

    for (int i = 1; i <= n; ++i) {
        int v = s_int[i - 1];
        for (int j = 0; j < 26; ++j) {
            if (j == v) {
                cnt[i][j] = cnt[i - 1][j] + 1;
            } else {
                cnt[i][j] = cnt[i - 1][j];
            }
        }
        A[i] = A[i - 1];
        for (int j = v + 1; j < 26; ++j) {
            A[i] += cnt[i][j];
        }
    }

    auto calc = [&](int mid, int r) {
        mid += 1;
        r += 1;

        vector<long long> tot(26), left(26), right(26);
        for (int j = 0; j < 26; ++j) {
            tot[j] = cnt[r][j];
            left[j] = cnt[mid - 1][j];
            right[j] = tot[j] - left[j];
        }

        long long sub = 0, cur = 0;
        for (int j = 24; j >= 0; --j) {
            cur += left[j + 1];
            sub += right[j] * cur;
        }

        return A[r] - sub;
    };

    long long res = inf;

    for (int r = 0; r < n; ++r) {
        int left = 0, right = r;
        while (left < right) {
            int mid = (left + right) >> 1;
            if (calc(mid, r) < x) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        for (int i = left - 1; i <= left + 1; ++i) {
            if (i >= 0 && i <= r) {
                res = min(res, abs(calc(i, r) - x));
            }
        }

        left = 0, right = r;
        while (left < right) {
            int mid = (left + right) >> 1;
            if (calc(mid, r) <= x) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        for (int i = left - 1; i <= left + 1; ++i) {
            if (i >= 0 && i <= r) {
                res = min(res, abs(calc(i, r) - x));
            }
        }
    }

    cout << res << "\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);

    solve(0);

    return 0;
}