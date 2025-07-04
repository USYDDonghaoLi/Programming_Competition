#include <bits/stdc++.h>
using namespace std;
#define N 51
#define INF (int)1e+9
#define rep(i, n) for(int i = 0; i < n; ++i)
#define rep2(i, a, b) for(int i = a; i <= b; ++i)
#define rep3(i, a, b) for(int i = a; i >= b; --i)
int main() {
	int n, m, k;
	string s, t;
	string c[N], a[N];
	int len[N];
	int dp1[N][N][26];
	int dp[N][N][N];
	vector<int>e[26];
	priority_queue<pair<int, int> >pq;
	pair<int, int>p;
	int sz[26];
	int x;
	cin >> s;
	cin >> t;
	cin >> k;
	rep(i, k) {
		cin >> c[i] >> a[i];
		len[i] = a[i].size();
		if (len[i] == 1)e[a[i][0] - 'a'].push_back(c[i][0] - 'a');
	}

	rep(i, 26)sz[i] = e[i].size();
	n = t.size();
	rep(i, n)rep2(j, i, n - 1)rep(ii, 26)dp1[i][j][ii] = INF;
	rep3(i, n - 1, 0) {
		rep2(j, i, n - 1)rep(ii, k)rep(jj, len[ii]){
			if (dp[j][ii][jj] != INF) printf("%d %d %d %d %d\n", i, j, ii, jj, dp[j][ii][jj]);
			dp[j][ii][jj] = INF;
		}
		rep2(j, i, n - 1) {
			if (j == i) {
				dp1[i][j][t[j] - 'a'] = 0;
				pq.push({ 0,t[j] - 'a' });
			}
			else {
				rep(ii, k) {
					rep2(jj, 1, len[ii] - 1) {
						rep2(kk, i, j - 1) {
							if ((dp[kk][ii][jj - 1] < INF) && (dp1[kk + 1][j][a[ii][jj] - 'a'] < INF)) {
								dp[j][ii][jj] = min(dp[j][ii][jj], dp[kk][ii][jj - 1] + dp1[kk + 1][j][a[ii][jj] - 'a']);
							}
						}
					}
					if (dp[j][ii][len[ii] - 1] + 1 < dp1[i][j][c[ii][0] - 'a']) {
						dp1[i][j][c[ii][0] - 'a'] = dp[j][ii][len[ii] - 1] + 1;
						pq.push({ -dp1[i][j][c[ii][0] - 'a'],c[ii][0] - 'a' });
					}
				}
			}
			while (!pq.empty()) {
				p = pq.top();
				pq.pop();
				if (p.first == -dp1[i][j][p.second]) {
					x = p.second;
					rep(ii, sz[x]) {
						if (dp1[i][j][x] + 1 < dp1[i][j][e[x][ii]]) {
							dp1[i][j][e[x][ii]] = dp1[i][j][x] + 1;
							pq.push({ -dp1[i][j][e[x][ii]],e[x][ii] });
						}
					}
				}
			}
			rep(ii, k)dp[j][ii][0] = dp1[i][j][a[ii][0] - 'a'];
		}
	}
	m = s.size();
	rep(i, n + 1)rep(jj, m + 1)dp[i][k][jj] = INF;
	dp[0][k][0] = 0;
	rep(i, n) {
		rep(jj, m) {
			rep(j, i + 1) {
				dp[i + 1][k][jj + 1] = min(dp[i + 1][k][jj + 1], dp[j][k][jj] + dp1[j][i][s[jj] - 'a']);
			}
		}
	}
	if (dp[n][k][m] == INF)cout << -1 << endl;
	else cout << dp[n][k][m] << endl;
	return 0;
}
