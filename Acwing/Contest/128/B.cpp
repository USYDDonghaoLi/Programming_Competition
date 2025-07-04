#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

using namespace std;

vector<int> prime_sieve(int n) {
    bool flag = n % 6 == 2;
    vector<bool> sieve(n / 3 + flag, false);
    vector<int> primes;

    for (int i = 1; i <= sqrt(n) / 3 + 1; ++i) {
        if (!sieve[i]) {
            int k = 3 * i + 1 | 1;
            for (int j = k * k / 3; j < n / 3 + flag; j += 2 * k)
                sieve[j] = true;
            for (int j = k * (k - 2 * (i & 1) + 4) / 3; j < n / 3 + flag; j += 2 * k)
                sieve[j] = true;
        }
    }

    if (n > 1) primes.push_back(2);
    if (n > 2) primes.push_back(3);

    for (int i = 1; i < n / 3 + (n % 6 == 1); ++i) {
        if (!sieve[i])
            primes.push_back(3 * i + 1 | 1);
    }
    
    return primes;
}

vector<pair<int, int>> prime_factorization(int num, const vector<int>& primes) {
    vector<pair<int, int>> factors;

    for (auto prime : primes) {
        if (prime * prime > num)
            break;

        if (num % prime == 0) {
            factors.push_back({prime, 0});
            while (num % prime == 0) {
                factors.back().second++;
                num /= prime;
            }
        }
    }

    if (num != 1)
        factors.push_back({num, 1});
    
    return factors;
}

bool solve(int a, int b, const vector<int>& primes) {
    if (a > b) swap(a, b);
    if (a == 1) return b == 1;

    auto factors = prime_factorization(a, primes);

    for (auto& [prime, cnta] : factors) {
        int cntb = 0;
        while (b % prime == 0) {
            cntb++;
            b /= prime;
        }
        if (cntb == 0) return false;

        while (cnta > 0 && cntb > 0) {
            if (cnta >= cntb) {
                cnta -= 2;
                cntb -= 1;
            } else {
                cnta -= 1;
                cntb -= 2;
            }
        }
        if (cnta != 0 || cntb != 0) return false;
    }
    return b == 1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    
    auto primes = prime_sieve(100000);

    while (t--) {
        int a, b;
        cin >> a >> b;
        cout << (solve(a, b, primes) ? "Yes" : "No") << '\n';
    }
    
    return 0;
}
