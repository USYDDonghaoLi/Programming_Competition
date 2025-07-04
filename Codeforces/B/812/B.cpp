#include<bits/stdc++.h>
using namespace std;

const int N = 100010;
int n, a[N];

void solve(){
    cin >> n;
    for (int i = 0; i < n; ++i) cin >> a[i];
    int idx = 0;
    for (;idx < n - 1 && a[idx] <= a[idx + 1];) ++idx;
    for (;idx < n - 1 && a[idx] >= a[idx + 1];) ++idx;
    cout << (idx == n - 1 ? "YES" : "NO") << "\n";
}

int main(){
    int T;
    cin >> T;
    for (;T--;) solve();
    return 0;
}