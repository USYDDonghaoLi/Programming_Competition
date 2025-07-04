#include<bits/stdc++.h>

using namespace std;


int n;
int * A;
unordered_map<int, vector<int>> adj;
long long * cost;


bool check(long long num)
{
    queue<int> q;
    unordered_set<int> ss;
    for (int i = 0; i < n; i ++)
    {
        if (cost[i] <= num)
        {
            q.push(i);
            ss.insert(i);
        }
    }
    
    long long cc[n];
    for (int i = 0; i < n; i ++)
    {
        cc[i] = cost[i];
    }
    
    while (!q.empty())
    {
        int x = q.front();    q.pop();
        for (int y: adj[x])
        {
            if (ss.find(y) == ss.end())
            {
                cc[y] -= A[y];
                if (cc[y] <= num)
                {
                    q.push(y);
                    ss.insert(y);
                }
            }
        }
    }
    return (int)ss.size() != n;
    
}


int main()
{
    std::ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    
    int m;
    cin >> n >> m;
    
    A = new int[n];
    for (int i = 0; i < n; i ++)
    {
        cin >> A[i];    
    }
    

    cost = new long long[n];
    for (int i = 0; i < n; i ++)
    {
        cost[i] = 0LL;
    }
    
    for (int _ = 0; _ < m; _ ++)
    {
        int u, v;
        cin >> u >> v;
        u --;
        v --;
        adj[u].push_back(v);
        adj[v].push_back(u);
        cost[u] += A[v];
        cost[v] += A[u];
    }
    
    if (m == 0)
    {
        cout << 0 << endl;
        return 0;
    }
    
    long long l = 1LL,  r = (long long)(1e12);
    while (l < r)
    {
        long long mid = (l + r) >> 1;
        if (check(mid) == true)
        {
            l = mid + 1;
        }else{
            r = mid;
        }
    }
    
    cout << l << endl;
    
    
    return 0;
}

