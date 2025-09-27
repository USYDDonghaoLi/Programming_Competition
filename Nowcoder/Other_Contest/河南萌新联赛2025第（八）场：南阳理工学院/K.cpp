#include <iostream>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int t;
    cin >> t;
    while (t--) {
        int n, k;
        cin >> n >> k;
        if (n == 1){
            cout << "YES\n";
            continue;
        }
        cout << (2 * n <= k ? "YES" : "NO") << "\n";
    }
    return 0;
}