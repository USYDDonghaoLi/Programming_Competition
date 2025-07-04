#include<bits/stdc++.h>
using namespace std;

class Prime {
private:
    vector<int> primes;
public:
    vector<int> prime_list(int n) {
        vector<int> res;
        if (n > 1) res.push_back(2);
        if (n > 2) res.push_back(3);
        // simplified version of prime_sieve method from Python, not 1:1 translation
        for(int i = 4; i <= n; ++i) {
            bool prime = true;
            for(int j = 2; j * j <= i; ++j) {
                if(i % j == 0) {
                    prime = false;
                    break;
                }
            }
            if(prime) res.push_back(i);
        }
        return res;
    }

    Prime(int n) {
        primes = prime_list(n);
    }

    vector<pair<int, int>> dissolve(int num) {
        vector<pair<int, int>> lst;
        for (auto prime: primes) {
            if (prime * prime > num) break;

            if (num % prime == 0) {
                lst.push_back({prime, 0});
                while(num % prime == 0) {
                    lst.back().second++;
                    num /= prime;
                }
            }
        }
        if (num != 1) lst.push_back({num, 1});
        return lst;
    }

    vector<int> get_divisors(int num) {
        vector<int> res = {1};
        for (auto [a, b]: dissolve(num)) {
            int m = res.size();
            int t = a;
            for(int i = 0; i < b; ++i) {
                for(int j = 0; j < m; ++j) {
                    res.push_back(res[j] * t);
                }
                t *= a;
            }
        }
        return res;
    }
};

int main() {
    ios_base::sync_with_stdio(false); 
    cin.tie(NULL);

    int T; cin >> T;
    Prime P(1010);
    while(T--) {
        int n; cin >> n;
        if(n == 1) {
            cout << 'a' << '\n';
            continue;
        }

        unordered_map<int, unordered_set<int>> adj;  // Change set to unordered_set
        
        auto a = P.get_divisors(n);
        sort(a.begin(), a.end());

        vector<int> res(n + 1, -1);
        vector<int> idxs(n);
        iota(idxs.begin(), idxs.end(), 1); // fill idxs with values from 1 to n

        for(auto idx: idxs) {
            unordered_set<int> S;  // Change set to unordered_set
            for(int i = 0; i < 26; ++i) S.insert(i);

            for(auto d: a) {
                if (idx <= d) break;
                if(res[idx - d] != -1) S.erase(res[idx - d]);
            }

            assert(!S.empty());
            res[idx] = *S.begin();
        }

        for(int i = 1; i <= n; ++i) {
            cout << char('a' + res[i]);
        }
        cout << '\n';
    }
    return 0;
}
