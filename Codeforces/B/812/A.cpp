#include <bits/stdc++.h>
using namespace std;

int n, x, y;

void solve(){
	cin >> n;
	int mx = 0, Mx = 0, my = 0, My = 0;
	for (int i = 0; i < n; ++i){
		cin >> x >> y;
		mx = min(mx, x);
		my = min(my, y);
		Mx = max(Mx, x);
		My = max(My, y);
	}
	
	cout << (Mx + My - mx - my) * 2 << "\n";
}

int main(){
	int T;
	cin >> T;
	for (; T--; ) solve();
	return 0;
}