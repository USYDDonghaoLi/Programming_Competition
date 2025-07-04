#pragma GCC optimize(1)
#pragma GCC optimize(2)
#pragma GCC optimize(3,"Ofast","inline")

#include <bits/stdc++.h>
using namespace std;

const int N = 55;
int n, a[N], b[N];

void solve(){
    cin >> n;
    int ma = 0x3f3f3f3f, mb = 0x3f3f3f3f;
    for (int i = 0; i < n; ++i) {cin >> a[i]; ma = min(ma, a[i]);}
    for (int i = 0; i < n; ++i) {cin >> b[i]; mb = min(mb, b[i]);}

    long long res = 0;
    for (int i = 0; i < n; ++i) res += max(a[i] - ma, b[i] - mb);
    cout << res << "\n";
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0);
    int T = 1;
    cin >> T;
    for (;T--;) solve();
    return 0;
}