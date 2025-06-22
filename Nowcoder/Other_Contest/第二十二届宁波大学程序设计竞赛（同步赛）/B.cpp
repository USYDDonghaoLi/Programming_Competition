#include<iostream>
#include<vector>
using namespace std;

vector<vector<int>> mul(vector<vector<int>> A, vector<vector<int>> B){
    int n = A.size();
    vector<vector<int>> res(n, vector<int>(n, 0));

    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) for (int k = 0; k < n; k++) res[i][j] |= A[i][k] & B[k][j];

    return res;
}

int main(){

    int n, m, q; cin >> n >> m >> q;

    vector<vector<int>> A(n, vector<int>(n, 0));

    for (int i = 0; i < m; i++){
        int u, v; cin >> u >> v;
        u--;
        v--;
        A[u][v] = 1;
    }

    vector<vector<vector<int>>> pws(30, vector<vector<int>>(n, vector<int>(n, 0)));

    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            pws[0][i][j] = A[i][j];
        }
    }

    for (int k = 1; k < 30; k++){
        vector<vector<int>> ans = mul(pws[k - 1], pws[k - 1]);
        for (int i = 0; i < n; i++){
            for (int j = 0; j < n; j++){
                pws[k][i][j] = ans[i][j];
            }
        }
    }

    while (q--){
        int x, k; cin >> x >> k;
        x--;

        vector<vector<int>> ans(n, vector<int>(n, 0));
        for (int i = 0; i < n; i++) ans[i][i] = 1;

        for (int bit = 0; bit < 30; bit++){
            if (k >> bit & 1){
                ans = mul(ans, pws[bit]);
            }
        }

        int res = 0;
        for (int y = 0; y < n; y++){
            if (ans[x][y]){
                res++;
            }
        }

        if (!res){
            cout << res << "\n";
        }
        else{
            cout << res << " ";
            for (int y = 0; y < n; y++){
                if (ans[x][y]){
                    res--;
                    cout << y + 1 << " \n"[res == 0];
                }
            }
        }
    }

    return 0;
}