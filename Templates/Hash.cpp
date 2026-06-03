#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using u64 = uint64_t;
using p64 = pair<u64, u64>;

mt19937_64 rng(chrono::steady_clock::now().time_since_epoch().count());

struct custom_hash {
    static uint64_t splitmix64(uint64_t x) {
        x += 0x9e3779b97f4a7c15;
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9;
        x = (x ^ (x >> 27)) * 0x94d049bb133111eb;
        return x ^ (x >> 31);
    }

    size_t operator()(uint64_t x) const {
        static const uint64_t FIXED_RANDOM = chrono::steady_clock::now().time_since_epoch().count();
        return splitmix64(x + FIXED_RANDOM);
    }

    size_t operator()(const p64& p) const {
        static const uint64_t FIXED_RANDOM = chrono::steady_clock::now().time_since_epoch().count();
        return splitmix64(p.first + FIXED_RANDOM) ^ splitmix64(p.second + FIXED_RANDOM);
    }
};

struct Hash {
    vector<u64> h1, pw1, h2, pw2;
    u64 b1, b2;
    Hash(const vector<int>& arr) {
        int n = arr.size();
        b1 = rng() | 1ULL;
        b2 = rng() | 1ULL;
        pw1.assign(n + 1, 1ULL);
        pw2.assign(n + 1, 1ULL);
        h1.assign(n + 1, 0ULL);
        h2.assign(n + 1, 0ULL);
        for (int i = 1; i <= n; i++) {
            pw1[i] = pw1[i - 1] * b1;
            pw2[i] = pw2[i - 1] * b2;
        }
        for (int i = 0; i < n; i++) {
            h1[i + 1] = h1[i] * b1 + (u64)arr[i];
            h2[i + 1] = h2[i] * b2 + (u64)arr[i];
        }
    }
    p64 GetHash(int l, int r) { // [l, r)
        u64 v1 = h1[r] - h1[l] * pw1[r - l];
        u64 v2 = h2[r] - h2[l] * pw2[r - l];
        return {v1, v2};
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int n, m, k;
    cin >> n >> m >> k;
    string t;
    cin >> t;
    vector<int> s(n);
    for (int i = 0; i < n; i++) {
        s[i] = t[i] - '0';
    }
    Hash H(s);
    unordered_map<p64, vector<int>, custom_hash> mp;
    int l = 0, r = m - 1;
    while (r < n) {
        p64 val = H.GetHash(l, r + 1);
        mp[val].push_back(l);
        l++;
        r++;
    }
    ll res = 0;
    for (const auto& p : mp) {
        const vector<int>& vec = p.second;
        int cur = -1;
        int cnt = 0;
        for (int idx : vec) {
            if (idx > cur) {
                cnt++;
                cur = idx + m - 1;
            }
        }
        if (cnt == k) {
            res++;
        }
    }
    cout << res << '\n';
}