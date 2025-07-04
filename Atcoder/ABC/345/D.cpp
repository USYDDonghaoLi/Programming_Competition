#include <iostream>
#include <vector>
#include <functional> // For std::function

using namespace std;

struct Rect {
    int w, h;
    Rect() : w(0), h(0) {} 
    Rect(int width, int height) : w(width), h(height) {}
};

bool canPlaceRects(int n, int W, int H, vector<Rect>& rects) {
    int area = W * H;
    int tot = 0;
    for(auto& r : rects){
        tot += r.h * r.w;
    }

    if (tot != area) {
        return false;
    }

    vector<vector<bool>> grid(H, vector<bool>(W, false));

    function<bool(int)> TRY;
    TRY = [&](int idx) -> bool {
        if (idx == rects.size()) {
            return true;
        } else {
            vector<vector<int>> mp(H + 1, vector<int>(W + 1, 0));
            for (int i = 1; i <= H; ++i) {
                for (int j = 1; j <= W; ++j) {
                    mp[i][j] = mp[i - 1][j] + mp[i][j - 1] - mp[i - 1][j - 1] + grid[i - 1][j - 1];
                }
            }

            auto& rect = rects[idx];
            for (int rotate = 0; rotate < 2; ++rotate) {
                int x = rect.w, y = rect.h;
                if (rotate) swap(x, y);

                for (int i = 0; i <= H - x; ++i) {
                    for (int j = 0; j <= W - y; ++j) {
                        if (mp[i + x][j + y] - mp[i][j + y] - mp[i + x][j] + mp[i][j] == 0) {
                            for (int k = i; k < i + x; ++k) {
                                for (int l = j; l < j + y; ++l) {
                                    grid[k][l] = true;
                                }
                            }
                            
                            if (TRY(idx + 1)) {
                                return true;
                            }
                            
                            for (int k = i; k < i + x; ++k) {
                                for (int l = j; l < j + y; ++l) {
                                    grid[k][l] = false;
                                }
                            }
                        }
                    }
                }

                swap(rect.w, rect.h); // Rotate back for the next iteration
            }

            return false;
        }
    };

    return TRY(0);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, W, H;
    cin >> n >> W >> H;

    vector<Rect> rects(n);
    for (int i = 0; i < n; ++i) {
        cin >> rects[i].w >> rects[i].h;
    }

    for (int i = 0; i < (1 << n); i++){
        vector<Rect> valid;
        for (int j = 0; j < n; j++){
            if ((i >> j) & 1){
                valid.emplace_back(rects[j]);
            }
        }
        if (canPlaceRects(n, W, H, valid)) {
            // cout << i << "\n";
            cout << "Yes\n";
            return 0;
        } 
    }

    cout << "No\n";

    return 0;
}
