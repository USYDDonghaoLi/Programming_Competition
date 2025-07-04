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
const int N = 1000010;

int dir[4][2] = {1, 0, -1, 0, 0, -1, 0, 1};

void solve(int testcase){
    int n;
    cin >> n;
    vector<int> A(n);
    for (int i = 0; i < n; i++){
        cin >> A[i];
    }

    vector<long long> weight(N), cnt(N);

    for (int a: A){
        for (int i = a; i < N; i += a){
            weight[i] += 1;
        }
        cnt[a] += 1;
    }

    for (int i = 1; i < N; i++){
        weight[i] += weight[i - 1];
    }

    long long res = 0;
    for (int a: A){
        res = res + weight[a];
    }

    for (int c: cnt){
        res = res - c * c;
        res = res + (c - 1) * c / 2;
    }

    cout << res << "\n";
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0); cout.tie(0);
    int T = 1;
    //cin >> T;
    for (int testcase = 1; testcase <= T; testcase++) solve(testcase);
    return 0;
}