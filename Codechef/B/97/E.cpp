#pragma GCC optimize(1)
#pragma GCC optimize(2)
#pragma GCC optimize(3,"Ofast","inline")
#include<bits/stdc++.h>
using namespace std;

long long quickpow(long long a, long long b, long long mod){
    long long ans;
    for (ans = 1; b; b >>= 1){
        if (b & 1){
            ans = (ans * a) % mod;
        }
        a = (a * a) % mod;
    }
    return ans;
}

template <class T>
void chmin(T &a, T b){
    if (b < a) a = b;
}
template <class T>
void chmax(T &a, T b){
    if (b > a) a = b;
}

const int inf = 0x3f3f3f3f;
const long long infl = 0x3f3f3f3f3f3f3f3f;

int dir[4][2] = {1, 0, -1, 0, 0, -1, 0, 1};

void solve(int testcase){
    int n, q;
    cin >> n >> q;
    vector<int> A(n, 0);

    for (int i = 0; i < n; i++){
        cin >> A[i];    
    }
    sort(A.begin(), A.end());

    long long tot = 1LL * n * (n - 1) * (n - 2) / 6
    for (int i = 0; i < q; i++){
        int k;
        cin >> k;
        int l = A[0],r = A[n - 1];
        while (l < r){
            int mid = l + r >> 1;
            int idx = distance(A.begin(), upper_bound(A.begin(), A.end(), mid));
            long long check = 1LL * (n - idx) * (n - idx - 1) * (n - idx - 2) / 6;
            if (tot - check < k){
                l = mid + 1;
            }
            else{
                r = mid;
            }
            cout << l << "\n";
        }
    }
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0); cout.tie(0);
    int T = 1;
    cin >> T;
    for (int testcase = 1; testcase <= T; testcase++) solve(testcase);
    return 0;
}