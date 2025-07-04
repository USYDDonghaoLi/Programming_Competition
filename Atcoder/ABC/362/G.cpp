#include <bits/stdc++.h>
using namespace std;

using ll = long long;

const int N = 2e6 + 5;
char t[N],s[N*10];

struct Aho_Corasick_Automaton{
    int nxt[N][26], fail[N], cnt[N], a[N], id[N];
    int root, idx, timer;

    void clear(){
    	memset(nxt[0],0,sizeof(nxt[0]));
    	root = idx = 0;
    }
    int newnode(){
    	idx++; memset(nxt[idx],0,sizeof(nxt[idx]));
    	return idx;
    }
    int insert(int pre, int ch){
        return nxt[pre][ch]?nxt[pre][ch]: nxt[pre][ch] = newnode();
    }
    int insert(char *s, int u){
    	int now = root;
    	for(int i = 0 ; s[i] ; i ++){
    	    now = insert(now, s[i]-'a');
    	}
    	return id[u] = now;
    }
    void build(){
    	fail[root] = root;
    	queue<int>q;
    	for(int i = 0 ; i < 26 ; i ++) if(nxt[0][i]) q.push(nxt[0][i]);
    	while(!q.empty()){
    		int h = q.front(); q.pop();
    		a[timer++] = h;
    		for(int i = 0 ; i < 26 ; i ++){
    			if(!nxt[h][i]){
    				nxt[h][i] = nxt[fail[h]][i];
    			}
    			else{
    				int tmp = nxt[h][i];
	    			fail[tmp] = nxt[fail[h]][i];
	    			q.push(tmp);
    			}
    		}
    	}
    }
    void solve(char *s, int m){
    	int now = root;
    	for(int i = 0 ; s[i] ; i ++){
    		now = nxt[now][s[i]-'a'];
    		cnt[now]++;
    	}
    	for(int i = timer ; i ; i --) cnt[fail[a[i]]] += cnt[a[i]];
    	for(int i = 0 ; i < m ; i ++) cout << cnt[id[i]] << '\n';
    }
}sol;

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(0);
    sol.clear();
    cin >> s;
    
    int n; cin >> n;
    for(int i = 0 ; i < n ; i ++){
    	cin >> t; sol.insert(t,i);
    }
    sol.build();
    
    sol.solve(s, n);

    return 0;
}