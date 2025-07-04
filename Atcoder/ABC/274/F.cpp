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
constexpr int N = 2010;
constexpr double eps = 1e-8;
double f[N][3];

void solve(){
    int n;
	double a;
    cin >> n >> a;
    for (int i = 0; i < n; i++){
        cin >> f[i][0] >> f[i][1] >> f[i][2];
    }

    double res = 0;
    for (int i = 0; i < n; i++){
        double x1 = f[i][1], v1 = f[i][2];
        vector<vector<double>> g;
        double t = 0;
        for (int j = 0; j < n; j++){
            double w2 = f[j][0], x2 = f[j][1], v2 = f[j][2];
            if (v1 == v2){
                if(x1 <= x2 && x2 <= x1 + a){
                    t += w2;
                }
            }
            else if(v1 > v2){
                if (x1 > x2){continue;}
                else{
                    double dx = x2 - x1;
                    double dv = v1 - v2;
                    double timea = 0, timeb = 0;
                    chmax(timea, (dx - a) / dv);
                    chmax(timeb, dx / dv);
                    g.push_back({timea, -w2});
                    g.push_back({timeb + eps, w2});
                }
            }
            else{
                if (x1 < x2) {
                    if (x2 <= x1 + a){
                        double dx = x2 - x1;
                        double dv = v2 - v1;
                        double timea = 0, timeb = 0;
                        chmax(timeb, (a - dx) / dv);
                        g.push_back({timea, -w2});
                        g.push_back({timeb + eps, w2});
                    }
                }
                else{
                    double dx = x1 - x2;
                    double dv = v2 - v1;
                    double timea = 0, timeb = 0;
                    chmax(timea, dx / dv);
                    chmax(timeb, (dx + a) / dv);
                    g.push_back({timea, -w2});
                    g.push_back({timeb + eps, w2});
                }
            }
        }
        sort(g.begin(), g.end());
        chmax(res, t);
        for (auto& gg: g){
            t -= gg[1];
            chmax(res, t);
        }
    }
    cout << (int)res << "\n";
}

int main(){
    ios_base::sync_with_stdio(0); cin.tie(0);
    int T = 1;
    //cin >> T;
    for (;T--;) solve();
    return 0;
}