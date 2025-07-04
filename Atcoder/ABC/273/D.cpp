#include<bits/stdc++.h>
using namespace std;

void solve(){
    int h, w, sx, sy;
    cin >> h >> w >> sx >> sy;
    unordered_map<int, vector<int>> rows;
    unordered_map<int, vector<int>> cols;
    
    int n;
    cin >> n;

    for (int _ = 0; _ < n; _ ++){
        int r, c;
        cin >> r >> c;
        rows[r].push_back(c);
        cols[c].push_back(r);
    }

    unordered_set<int> Sx;
    unordered_set<int> Sy;

    int q;
    cin >> q;
    int x = sx;
    int y = sy;
    for (int _ = 0; _ < q; _ ++){
        char d;
        int lc;
        cin >> d >> lc;
        if (d == 'L'){
            if (Sx.find(x) == Sx.end()){
                Sx.insert(x);
                rows[x].push_back(0);
                rows[x].push_back(w + 1);
                sort(rows[x].begin(), rows[x].end());
            }
            int idx = lower_bound(rows[x].begin(), rows[x].end(), y) - rows[x].begin() - 1;
            int left = rows[x][idx];
            if (y - (left + 1) >= lc){
                y -= lc;
            }else{
                y = left + 1;
            }
        }else if (d == 'R'){
            if (Sx.find(x) == Sx.end()){
                Sx.insert(x);
                rows[x].push_back(0);
                rows[x].push_back(w + 1);
                sort(rows[x].begin(), rows[x].end());
            }
            int idx = lower_bound(rows[x].begin(), rows[x].end(), y) - rows[x].begin();
            int right = rows[x][idx];
            if ((right - 1) - y >= lc){
                y += lc;
            }else{
                y = right - 1;
            }
        }else if (d == 'U'){
            if (Sy.find(y) == Sy.end()){
                Sy.insert(y);
                cols[y].push_back(0);
                cols[y].push_back(h + 1);
                sort(cols[y].begin(), cols[y].end());
            }
            int idx = lower_bound(cols[y].begin(), cols[y].end(), x) - cols[y].begin() - 1;
            int up = cols[y][idx];
            if (x - (up + 1) >= lc){
                x -= lc;
            }else{
                x = up + 1;
            }
        }else{
            if (Sy.find(y) == Sy.end()){
                Sy.insert(y);
                cols[y].push_back(0);
                cols[y].push_back(h + 1);
                sort(cols[y].begin(), cols[y].end());
            }
            int idx = lower_bound(cols[y].begin(), cols[y].end(), x) - cols[y].begin();
            int down = cols[y][idx];
            if ((down - 1 - x) >= lc){
                x += lc;
            }else{
                x = down - 1;
            }            
        }
        cout << x << ' ' << y << endl;
    }


}

int main(){
    std::ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);

    solve();

    return 0;;
}
