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

template<typename T>
class SegTree {
private:
    std::vector<T> d;
    std::function<T(T, T)> op;
    T e;
    int size, n, log;
    
    void update(int k) {
        d[k] = op(d[2 * k], d[2 * k + 1]);
    }

public:
    SegTree(std::vector<T>& V, std::function<T(T, T)> OP, T E)
        : op(OP), e(E) {
        n = V.size();
        log = std::ceil(std::log2(n));
        size = 1 << log;
        d = std::vector<T>(2*size, e);
        for(int i = 0; i < n; i++) {
            d[size + i] = V[i];
        }
        for(int i = size - 1; i > 0; i--) {
            update(i);
        }
    }

    void set(int p, T x) {
        assert(0 <= p && p < n);
        p += size;
        d[p] = x;
        for(int i = 1; i <= log; i++) {
            update(p >> i);
        }
    }

    T get(int p) {
        assert(0 <= p && p < n);
        return d[p + size];
    }

    T prod(int l, int r) {
        assert(0 <= l && l <= r && r <= n);
        T sml = e, smr = e;
        l += size;
        r += size;

        while(l < r) {
            if (l & 1) {
                sml = op(sml, d[l]);
                l++;
            }
            if (r & 1) {
                r--;
                smr = op(d[r], smr);
            }
            l >>= 1;
            r >>= 1;
        }
        return op(sml, smr);
    }

    T all_prod() {
        return d[1];
    }

    int max_right(int l, std::function<bool(T)> f) {
        assert(0 <= l && l <= n);
        assert(f(e));
        if(l == n) return n;
        l += size;
        T sm = e;
        do {
            while(l % 2 == 0) l >>= 1;
            if(!f(op(sm, d[l]))) {
                while(l < size) {
                    l = 2 * l;
                    if(f(op(sm, d[l]))) {
                        sm = op(sm, d[l]);
                        l++;
                    }
                }
                return l - size;
            }
            sm = op(sm, d[l]);
            l++;
        } while((l & -l) != l);
        return n;
    }

    int min_left(int r, std::function<bool(T)> f) {
        assert(0 <= r && r <= n);
        assert(f(e));
        if(r == 0) return 0;
        r += size;
        T sm = e;
        do {
            r--;
            while(r > 1 && (r % 2)) r >>= 1;
            if(!f(op(d[r], sm))) {
                while(r < size) {
                    r = (2 * r + 1);
                    if(f(op(d[r], sm))) {
                        sm = op(d[r], sm);
                        r--;
                    }
                }
                return r + 1 - size;
            }
            sm = op(d[r], sm);
        } while((r & -r) != r);
        return 0;
    }
};

const int inf = 0x3f3f3f3f;
const long long infl = 0x3f3f3f3f3f3f3f3f;

int dir[4][2] = {1, 0, -1, 0, 0, -1, 0, 1};

void solve(int testcase){
    int n, m, q;
    cin >> n >> m >> q;
    string s;
    cin >> s;
    
    set<int> S;
    for (int i = 0; i < n; i++){
        S.insert(i);
    }

    vector<int> v(n + 1, 0), order;

    for (int i = 0; i < m; i++){
        int l, r;
        cin >> l >> r;
        auto il = S.lower_bound(l), ir = S.upper_bound(r);
        vector<int> tmp;
        for (auto it = il; it != ir; it ++){
            tmp.emplace_back(*it);
        }
        for (int val: tmp){
            order.emplace_back(val);
            S.erase(val);
            v[val] = 1;
        }
    }

    for (int val: S){
        order.emplace_back(val);
    }

    unordered_map<int, int> d, dd;
    for (int i = 0; i < n; i++){
        d[order[i]] = i + 1;
        dd[i + 1] = order[i];
    }

    vector<int> news;
    int IN = 0, OUT = 0;
    for (auto& c: s) {
        news.emplace_back(c - '0');
        IN += news.back();
    }

    int LEN = IN;

    vector<int> V(n + 10, 0);
    for (int i = 1; i <= n; i++){
        if (s[dd[i]]){
            V[i] = 1;
        }
    }

    SegTree<int> sg(V, [](int x, int y){return x + y;}, 0);

    for (int i = 0; i < q; i++){
        int idx;
        cin >> idx;
        --idx;
        if (s[idx]){
            if (v[idx]){
                --IN;
            }
            else{
                --OUT;
            }
        }
        else{
            if (v[idx]){
                ++IN;
            }
            else{
                ++OUT;
            }
        }

        if (!IN && !OUT){
            cout << 0 << "\n";
        }
        else if (IN + OUT >= LEN){
            cout << LEN - IN << "\n";
        }
        else{
            cout << OUT + sg.prod(IN + OUT + 1, LEN + 1) << "\n";
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