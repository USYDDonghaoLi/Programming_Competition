#include<bits/stdc++.h>

using namespace std;

const int LOGN = 18;
const int N = (1 << LOGN);
const int MOD = 998244353;
const int g = 3;

#define forn(i, n) for(int i = 0; i < int(n); i++)

inline int mul(int a, int b)
{
    return (a * 1ll * b) % MOD;
}

inline int norm(int a) 
{
    while(a >= MOD)
        a -= MOD;
    while(a < 0)
        a += MOD;
    return a;
}

inline int binPow(int a, int k) 
{
    int ans = 1;
    while(k > 0) 
    {
        if(k & 1)
            ans = mul(ans, a);
        a = mul(a, a);
        k >>= 1;
    }
    return ans;
}

inline int inv(int a) 
{
    return binPow(a, MOD - 2);
}

vector<int> w[LOGN];
vector<int> iw[LOGN];
vector<int> rv[LOGN];

void precalc() 
{
    int wb = binPow(g, (MOD - 1) / (1 << LOGN));
    
    for(int st = 0; st < LOGN; st++) 
    {
        w[st].assign(1 << st, 1);
        iw[st].assign(1 << st, 1);
        
        int bw = binPow(wb, 1 << (LOGN - st - 1));
        int ibw = inv(bw);
        
        int cw = 1;
        int icw = 1;
        
        for(int k = 0; k < (1 << st); k++) 
        {
            w[st][k] = cw;
            iw[st][k] = icw;
            
            cw = mul(cw, bw);
            icw = mul(icw, ibw);
        }
        
        rv[st].assign(1 << st, 0);
        
        if(st == 0) 
        {
            rv[st][0] = 0;
            continue;
        }
        int h = (1 << (st - 1));
        for(int k = 0; k < (1 << st); k++)
            rv[st][k] = (rv[st - 1][k & (h - 1)] << 1) | (k >= h);
    }
}

inline void fft(int a[N], int n, int ln, bool inverse) 
{   
    for(int i = 0; i < n; i++) 
    {
        int ni = rv[ln][i];
        if(i < ni)
            swap(a[i], a[ni]);
    }
    
    for(int st = 0; (1 << st) < n; st++) 
    {
        int len = (1 << st);
        for(int k = 0; k < n; k += (len << 1)) 
        {
            for(int pos = k; pos < k + len; pos++) 
            {
                int l = a[pos];
                int r = mul(a[pos + len], (inverse ? iw[st][pos - k] : w[st][pos - k]));
                
                a[pos] = norm(l + r);
                a[pos + len] = norm(l - r);
            }
        }
    }
    
    if(inverse) 
    {
        int in = inv(n);
        for(int i = 0; i < n; i++)
            a[i] = mul(a[i], in);
    }
}

int aa[N], bb[N], cc[N];

vector<int> multiply(vector<int> a, vector<int> b) 
{
    int sza = a.size();
    int szb = b.size();
    int n = 1, ln = 0;
    while(n < (sza + szb))
        n <<= 1, ln++;
    for(int i = 0; i < n; i++)
        aa[i] = (i < sza ? a[i] : 0);
    for(int i = 0; i < n; i++)
        bb[i] = (i < szb ? b[i] : 0);
        
    fft(aa, n, ln, false);
    fft(bb, n, ln, false);
    
    for(int i = 0; i < n; i++)
        cc[i] = mul(aa[i], bb[i]);
        
    fft(cc, n, ln, true);
    
    int szc = n;
    vector<int> c(szc);
    szc = n;
    for(int i = 0; i < n; i++)
        c[i] = cc[i];
    return c;
}                    

int main()
{
    int n;
    cin >> n;
    vector<int> fact(n + 1);
    fact[0] = 1;
    for(int i = 0; i < n; i++)
        fact[i + 1] = mul(fact[i], i + 1);
    precalc();
    vector<int> A = {0, 1, 2};
    vector<int> B = {0, 1, 1};
    vector<int> C = {0, 1, 1};
    vector<int> D = {0, 1, 1};
    vector<int> conv;
    const int K = 2000;
    int last_conv = -1e9;
    while(A.size() <= n)
    {
        int cur = A.size();
        if(cur - last_conv >= K)
        {
            last_conv = cur - 1;
            conv = multiply(C, D);
        }
        /*for(auto x : conv) cerr << x << " ";
        cerr << endl;*/
        int val_A;
        if(last_conv * 2 >= cur)
        {
            val_A = conv[cur];
            // [cur - last_conv, last_conv] are already used
            for(int i = 1; i < (cur - last_conv); i++)
            {
                val_A = norm(val_A + mul(C[i], D[cur - i]));
            }
            for(int i = last_conv + 1; i < cur; i++)
            {
                val_A = norm(val_A + mul(C[i], D[cur - i]));
            }
        }
        else
        {
            val_A = 0;
            for(int i = 1; i <= cur - 1; i++)
            {
                val_A = norm(val_A + mul(C[i], D[cur - i]));
            }
        }
        val_A = mul(val_A, fact[cur - 1]);
        val_A = mul(val_A, 2);
        A.push_back(val_A);
        B.push_back(mul(val_A, inv(2)));
        C.push_back(mul(val_A, inv(fact[cur])));
        D.push_back(mul(B.back(), inv(fact[cur - 1])));
    }
    cout << norm(A[n] - 2) << endl;
}