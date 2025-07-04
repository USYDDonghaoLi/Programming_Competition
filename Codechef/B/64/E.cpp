#pragma GCC optimize(1)
#pragma GCC optimize(2)
#pragma GCC optimize(3,"Ofast","inline")
#include<bits/stdc++.h>
using namespace std;

template <class T>
void chmin(T &a, T b){
    if (b < a) a = b;
}
template <class T>
void chmax(T &a, T b){
    if (b > a) a = b;
}

const int N = 100010;
long long a[N];

long long calc(long long num){
    long long l = 0, r = 1000000010;
    while (l < r){
        long long mid = (l + r) >> 1;
        if (mid * mid <= num){
            l = mid + 1;
        }
        else{
            r = mid;
        }
    }
    return l - 1;
}

void solve(){
    int n;
    cin >> n;
    
    //最右侧的1 左边全是1
    a[0] = 1;
    int idx = 0;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        if (a[i] == 1) idx = i;
    }
    
    long long res = 0;
    for (int i = idx; i >= -1; i--){
        while (a[i] > 1){
            ++res;
            long long o = sqrt(a[i]);
            a[i] = calc(a[i]);
        }
    }
    
    unordered_map <long long, long long> mp;
    mp[1] = res;
    for (int i = idx + 1; i <= n; i++){
        unordered_map<long long, long long> mp2;
        long long now = a[i];
        long long step = 0;
        
        while (now > 1){
            for (auto& [p, q]: mp){
                if (now >= p){
                    if (mp2.find(now) == mp2.end()){
                        mp2[now] = step + q;
                    }
                    else{
                        chmin(mp2[now], step + q);
                    }
                }
            }
            
            long long t = now;
            long long step2 = step;
            
            while (t < 1e9){
                ++step2;
                t = t * t;
                for (auto& [p, q]: mp){
                    if (t >= p){
                        if (mp2.find(t) == mp2.end()){
                            mp2[t] = step2 + q;
                        }
                        else{
                            chmin(mp2[t], step2 + q);
                        }
                    }
                }
            }
            
            ++step;
            now = calc(now);
            
            if (now == 1){
                for (auto& [p, q]: mp){
                    if (now >= p){
                        if (mp2.find(now) == mp2.end()){
                            mp2[now] = step + q;
                        }
                        else{
                            chmin(mp2[now], step + q);
                        }
                    }
                }
            }
        }
        mp.swap(mp2);
    }
    
    long long final = 9e18;
    for(auto& [p, q]: mp) chmin(final, q);
    cout << final << "\n";
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0);
    int T = 1;
    cin >> T;
    for (;T--;) solve();
    return 0;
}