
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <cmath>
#include <climits>
#include <map>
#include <set>
#include <string>
#include <cstring>
#include <stack>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
using namespace std;

const int INF = 1000000;

int main(){
    
    string s;
    cin >> s;
    
    int n = s.size();
    vector<int> A(n);
    for (int i = 0; i < n; ++i){
        A[i] = s[i] - 'a';
    }
    
    int res = INF;
    
    for (int k = 0; k < 26; ++k){
        
        vector<vector<int>> B(n, vector<int>(26, INF));
        for (int j = 0; j < 26; ++j){
            if (A[0] == j){
                B[0][j] = 0;
            }
            else{
                B[0][j] = 1;
            }
        }
        
        for (int i = 1; i < n; ++i){
            for (int j = 0; j < 26; ++j){
                if (A[i] == j){
                    B[i][j] = min(B[i][j], B[i - 1][(j - k + 26) % 26]);
                    B[i][j] = min(B[i][j], B[i - 1][(j + k) % 26]);
                }
                else{
                    B[i][j] = min(B[i][j], B[i - 1][(j - k + 26) % 26] + 1);
                    B[i][j] = min(B[i][j], B[i - 1][(j + k) % 26] + 1);
                }
            }
        }
        
        for (int j = 0; j < 26; ++j){
            res = fmin(res, B[n - 1][j]);
        }
        
    }
    
    cout << res << "\n";
    
    return 0;
}