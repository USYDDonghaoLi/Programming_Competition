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

string change(long long num){
    string s;
    while (num){
        char ch += num % 10 + '0';
        s += ch;
    }
    return s;
}

void solve(int testcase){
    long long n, x;
    cin >> n >> x;

    queue<long long> q;
    
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0); cout.tie(0);
    int T = 1;
    cin >> T;
    for (int testcase = 1; testcase <= T; testcase++) solve(testcase);
    return 0;
}