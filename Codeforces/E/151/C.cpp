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
    string s;
    cin >> s;
    int n = s.size();

    vector<vector<int>> nxt(n + 1, vector<int>(10, inf));
    for (int i = n - 1; i >= 0; i--){
        for (int j = 0; j < 10; j++){
            nxt[i][j] = nxt[i + 1][j];
        }
        nxt[i][s[i] - '0'] = i + 1;
    }

    int m;
    cin >> m;
    string l;
    cin >> l;
    string r;
    cin >> r;

    queue<int> q;
    q.push(0);

    for (int i = 0; i < m; i++){
        int k = q.size();
        for (int _ = 0; _ < k; _++){
            int idx = q.front();
            q.pop();
            for (int j = l[i] - '0'; j <= r[i] - '0'; j++){
                int NEW = nxt[idx][j];
                if (NEW == inf){
                    cout << "YES" << "\n";
                    return;
                }
                q.push(NEW);
            }
        }
    }

    cout << "NO" << "\n";
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0); cout.tie(0);
    int T = 1;
    cin >> T;
    for (int testcase = 1; testcase <= T; testcase++) solve(testcase);
    return 0;
}