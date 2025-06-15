#include <bits/stdc++.h>
using namespace std;

#define ll long long
#define fmin(x, y) ((x) < (y) ? (x) : (y))
#define fmax(x, y) ((x) > (y) ? (x) : (y))

const ll inf = 1e18;

class Prime {
public:
    vector<int> primes;

    vector<bool> prime_sieve(int n) {
        bool flag = n % 6 == 2;
        vector<bool> sieve((n / 3 + flag + 7) / 8 + 1, false);
        for (int i = 1; i <= (int)sqrt(n) / 3 + 1; i++) {
            if (!(sieve[i / 8] & (1 << (i & 7)))) {
                int k = (3 * i + 1) | 1;
                for (int j = k * k / 3; j < n / 3 + flag; j += 2 * k)
                    sieve[j / 8] |= 1 << (j & 7);
                for (int j = k * (k - 2 * (i & 1) + 4) / 3; j < n / 3 + flag; j += 2 * k)
                    sieve[j / 8] |= 1 << (j & 7);
            }
        }
        return sieve;
    }

    vector<int> prime_list(int n) {
        vector<int> res;
        if (n > 1) res.push_back(2);
        if (n > 2) res.push_back(3);
        if (n > 4) {
            auto sieve = prime_sieve(n + 1);
            for (int i = 1; i < (n + 1) / 3 + (n % 6 == 1); i++) {
                if (!(sieve[i / 8] & (1 << (i & 7))))
                    res.push_back((3 * i + 1) | 1);
            }
        }
        return res;
    }

    Prime(int n) {
        primes = prime_list(n);
    }

    vector<pair<int, int>> dissolve(int num) {
        vector<pair<int, int>> lst;
        for (int prime : primes) {
            if (prime * prime > num) break;
            if (num % prime == 0) {
                lst.emplace_back(prime, 0);
                while (num % prime == 0) {
                    lst.back().second++;
                    num /= prime;
                }
            }
        }
        if (num != 1) lst.emplace_back(num, 1);
        return lst;
    }

    vector<int> GetAllFactors(int num, bool SORT = false) {
        vector<int> res = {1};
        if (num == 1) return res;
        for (auto [a, b] : dissolve(num)) {
            int mul = a;
            int k = res.size();
            for (int i = 0; i < b; i++) {
                for (int j = 0; j < k; j++)
                    res.push_back(res[j] * mul);
                mul *= a;
            }
        }
        if (SORT) sort(res.begin(), res.end());
        return res;
    }

    int primitive_root(int num) {
        int g = 1;
        auto DIS = dissolve(num);
        while (true) {
            bool ok = true;
            for (auto [a, b] : DIS) {
                ll pow_res = 1, base = g, exp = (num - 1) / a;
                while (exp) {
                    if (exp & 1) pow_res = pow_res * base % num;
                    base = base * base % num;
                    exp >>= 1;
                }
                if (pow_res == 1) {
                    ok = false;
                    break;
                }
            }
            if (ok) break;
            g++;
        }
        return g;
    }
};

Prime P(320);

void solve(int testcase) {
    int n, q;
    cin >> n >> q;
    vector<int> A(n);
    set<int> S;
    for (int i = 0; i < n; i++) {
        cin >> A[i];
        S.insert(A[i]);
    }

    map<int, vector<int>> mp;
    map<int, int> ptr;
    for (int i = 0; i < n; i++) {
        mp[A[i]].push_back(i);
        ptr[A[i]] = 0;
    }

    vector<tuple<int, int, int, int>> queries;
    for (int i = 0; i < q; i++) {
        int k, l, r;
        cin >> k >> l >> r;
        l--; r--;
        queries.emplace_back(l, r, k, i);
    }
    sort(queries.begin(), queries.end());

    vector<ll> res(q, 0);
    int prevl = 0;

    for (auto [l, r, k, index] : queries) {
        for (int j = prevl; j < l; j++) {
            ptr[A[j]]++;
        }
        prevl = l;

        vector<int> idxs;
        for (int d : P.GetAllFactors(k)) {
            if (S.find(d) == S.end()) continue;
            if (ptr[d] < (int)mp[d].size() && l <= mp[d][ptr[d]] && mp[d][ptr[d]] <= r)
                idxs.push_back(mp[d][ptr[d]]);
        }
        sort(idxs.begin(), idxs.end());

        int cur = l;
        for (int idx : idxs) {
            res[index] += (ll)k * (idx - cur);
            cur = idx;
            while (k % A[idx] == 0) k /= A[idx];
        }
        res[index] += (ll)k * (r - cur + 1);
    }

    for (ll x : res) cout << x << '\n';
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);

    int T;
    cin >> T;
    for (int t = 0; t < T; t++) solve(t);
    return 0;
}