#include <iostream>
#include <vector>
#include <unordered_map>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;
    string input;
    cin >> input;
    vector<int> A(n);
    for (int i = 0; i < n; ++i) {
        A[i] = input[i] - '0';
    }

    unordered_map<int, int> mp;
    vector<int> cmp;
    const int mod = 1'000'000'007;

    for (int i = n - 1; i >= 0; --i) {
        vector<int> ncmp;
        int a = A[i];
        for (int x : cmp) {
            int cc = (x * 10 + a) % mod;
            ncmp.push_back(cc);
            mp[cc]++;
        }
        if (a) {
            ncmp.push_back(a);
            mp[a]++;
        }
        cmp = ncmp;
    }

    long long ans = 0;
    vector<int> mp1;

    for (int i = 0; i < n; ++i) {
        int a = A[i];
        vector<int> nmp1;
        for (int x : mp1) {
            nmp1.push_back((x * 10 + a) % mod);
        }
        int cur = 0;
        int t = 1;
        for (int j = i; j < n; ++j) {
            cur = (cur + t * A[j]) % mod;
            t = t * 10 % mod;
            if (A[j]) {
                mp[cur]--;
            }
        }
        if (a) {
            nmp1.push_back(a);
            for (int x : nmp1) {
                if (mp.find(x) != mp.end()) {
                    ans += mp[x];
                }
            }
        }
        mp1 = nmp1;
    }

    cout << ans << endl;

    return 0;
}
