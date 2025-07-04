#pragma GCC optimize(1)
#pragma GCC optimize(2)
#pragma GCC optimize(3,"Ofast","inline")

#include <bits/stdc++.h>
using namespace std;

const int N = 55;
int n, a[N], f[N];

void solve(){
    memset(f, 0, sizeof(f));
    cin >> n;
    for (int i = 0; i < n; ++i) cin >> a[i], ++f[a[i]];
    
    int res = 0;
    for (int s = 2; s <= 2 * n; ++s){
        int temp = 0;
        for (int i = 1; i <= s / 2; ++i){
            if (s - i > n) continue;
            if (i + i == s) temp += f[i] / 2;
            else temp += min(f[i], f[s - i]);
        }
        res = max(res, temp);
    }

    cout << res << "\n";
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0);
    int T = 1;
    cin >> T;
    for (;T--;) solve();
    return 0;
}