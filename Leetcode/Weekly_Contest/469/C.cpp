#include <algorithm>

int dp[2][2010], ps[2][2010], ndp[2][2010], nps[2][2010];

class Solution {
public:
    int zigZagArrays(int n, int l, int r) {
        const int mod = 1e9 + 7;
        int tot = r - l + 1;

        if (n == 1){
            return tot;
        }
        else if (n == 2){
            return tot * (tot - 1) / 2;
        }
        else{
            
            r -= l;
            l = 0;
            // vector<vector<int>> dp(2, vector<int>(r + 1, 0));
            // vector<vector<int>> ps(2, vector<int>(r + 2, 0));

            for (int i = 0; i < 2; ++i){
                for (int j = 0; j <= r; ++j){
                    dp[i][j] = ps[i][j] = ndp[i][j] = nps[i][j] = 0;
                }
            }

            for (int j = 0; j <= r; ++j){
                dp[0][j] = j;
                ps[0][j + 1] = ps[0][j] + j;
                dp[1][j] = r - j;
                ps[1][j + 1] = ps[1][j] + r - j;
            }

            for (int i = 3; i <= n; ++i){
                // vector<vector<int>> ndp(2, vector<int>(r + 1, 0));
                // vector<vector<int>> nps(2, vector<int>(r + 2, 0));

                for (int j = 0; j <= r; j++){
                    if (j){
                        ndp[0][j] = ps[1][j];
                    }
                    nps[0][j + 1] = (ndp[0][j] + nps[0][j]) % mod;
                    if (j != r){
                        ndp[1][j] = (ps[0][r + 1] - ps[0][j + 1] + mod) % mod;
                    }
                    nps[1][j + 1] = (ndp[1][j] + nps[1][j]) % mod;
                }

                std::swap(dp, ndp);
                std::swap(ps, nps);
            }

            int res = 0;
            for (int i = 0; i < 2; ++i){
                for (int j = 0; j <= r; ++j){
                    res = (res + dp[i][j]) % mod;
                }
            }

            return res;
        }
    }
};