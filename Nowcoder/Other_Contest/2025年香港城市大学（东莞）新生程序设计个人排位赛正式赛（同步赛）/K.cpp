#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout << fixed << setprecision(6);
    int T;
    cin >> T;
    for (int t = 0; t < T; t++) {
        long long a, b, x1, y1, x2, y2;
        cin >> a >> b >> x1 >> y1 >> x2 >> y2;
        long long aa = abs(a), bb = abs(b);
        long long dx = x2 - x1;
        long long dy = y2 - y1;
        double cross = abs(x1 * y2 - x2 * y1);
        double tmp = sqrt((dx * 1.0 / aa) * (dx * 1.0 / aa) + (dy * 1.0 / bb) * (dy * 1.0 / bb));
        if (tmp == 0) {
            cout << -1 << "\n";
            continue;
        }
        double d = cross / (aa * bb * tmp);
        if (d >= 1.0 - 1e-9) {
            cout << -1 << "\n";
            continue;
        }
        double c = 2 * acos(d);
        double sinc = sin(c);
        double S = (c - sinc) / 2.0;
        double pi = acos(-1.0);
        double larger = pi - S;
        double ratio = S / larger;
        cout << ratio << "\n";
    }
    return 0;
}