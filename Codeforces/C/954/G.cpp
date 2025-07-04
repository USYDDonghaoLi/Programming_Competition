#include <bits/stdc++.h>
using namespace std;

class Prime {
public:
    Prime(int n) {
        primes = prime_list(n);
    }

    vector<int> prime_list(int n) {
        vector<int> res;
        if (n > 1) res.push_back(2);
        if (n > 2) res.push_back(3);
        if (n > 4) {
            auto sieve = prime_sieve(n + 1);
            for (int i = 1; 3 * i + 1 < n + 1; ++i) {
                if (!(sieve[i >> 3] >> (i & 7) & 1)) {
                    res.push_back(3 * i + 1 | 1);
                }
            }
        }
        return res;
    }

    vector<char> prime_sieve(int n) {
        bool flag = n % 6 == 2;
        vector<char> sieve((n / 3 + flag + 7) >> 3);
        for (int i = 1, end = int(sqrt(n) / 3); i <= end; ++i) {
            if (!(sieve[i >> 3] >> (i & 7) & 1)) {
                int k = 3 * i + 1 | 1;
                for (int j = k * k / 3; j < n / 3 + flag; j += 2 * k)
                    sieve[j >> 3] |= 1 << (j & 7);
                for (int j = k * (k - 2 * (i & 1) + 4) / 3; j < n / 3 + flag; j += 2 * k)
                    sieve[j >> 3] |= 1 << (j & 7);
            }
        }
        return sieve;
    }

    vector<pair<int, int>> dissolve(int num) {
        vector<pair<int, int>> lst;
        int idx = -1;
        for (int prime : primes) {
            if (prime * prime > num) break;
            if (num % prime == 0) {
                lst.push_back({prime, 0});
                ++idx;
            }
            while (num % prime == 0) {
                ++lst[idx].second;
                num /= prime;
            }
        }
        if (num != 1) lst.push_back({num, 1});
        return lst;
    }

    vector<int> GetAllFactors(int num, bool SORT = false) {
        if (factor_cache.find(num) != factor_cache.end()) {
            return factor_cache[num];
        }

        vector<int> res = {1};
        if (num == 1) return res;
        for (auto [a, b] : dissolve(num)) {
            int mul = a;
            int k = res.size();
            for (int _ = 0; _ < b; ++_) {
                for (int i = 0; i < k; ++i) {
                    res.push_back(res[i] * mul);
                }
                mul *= a;
            }
        }
        if (SORT) sort(res.begin(), res.end());
        factor_cache[num] = res;
        return res;
    }

private:
    vector<int> primes;
    unordered_map<int, vector<int>> factor_cache;
};

Prime P(400);

vector<vector<int>> factors(500010);

void solve() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    unordered_map<int, unordered_map<int, long long>> mp;
    
    for (int i = 1; i <= n; ++i) {
        int g = __gcd(nums[i - 1], i);
        mp[i / g][nums[i - 1] / g]++;
    }
    
    long long res = 0;
    
    for (auto& [i, inner_map] : mp) {
        for (auto& [v, count] : inner_map) {
            if (v % i == 0) {
                res -= count;
            }
            for (int f : factors[v]) {
                if (mp.find(f) != mp.end()) {
                    for (int mul = i; mul <= n; mul += i) {
                        if (mp[f].find(mul) != mp[f].end()) {
                            res += count * mp[f][mul];
                        }
                    }
                }
            }
        }
    }
    
    cout << res / 2 << "\n";
}

int32_t main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int t;
    cin >> t;
    for (int i = 1; i <= 500000; i++){
        factors[i] = P.GetAllFactors(i);
    }
    while (t--) {
        solve();
    }
    return 0;
}
