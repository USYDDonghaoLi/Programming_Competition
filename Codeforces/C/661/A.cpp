#pragma GCC optimize(1)
#pragma GCC optimize(2)
#pragma GCC optimize(3,"Ofast","inline")

#include <bits/stdc++.h>
using namespace std;

const int N = 1010;
int n, a[N];

void solve(){
    cin >> n;
    for (int i = 0; i < n; ++i) cin >> a[i];
    sort(a, a + n);
    for (int i = 1; i < n; ++i){
        if (a[i] - a[i - 1] > 1){cout << "NO" << "\n"; return;}
    }
    cout << "YES" << "\n";
    return;
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0);
    int T = 1;
    cin >> T;
    for (;T--;) solve();
    return 0;
}