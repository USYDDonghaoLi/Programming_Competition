#include <iostream>
#include <string>
#include <algorithm>
#include <unordered_map>
#include <vector>

using namespace std;

// Function to get the rank of a card
int getRank(char card, unordered_map<char, int>& rankMap) {
    return rankMap[card];
}

int main() {
    int t;
    cin >> t;

    // Mapping of card characters to their ranks
    string cards = "3456789XJQKA2MF";
    unordered_map<char, int> rankMap;
    for (int i = 0; i < cards.size(); ++i) {
        rankMap[cards[i]] = i;
    }

    while (t--) {
        string a, b;
        cin >> a >> b;

        // Special cases
        if ((a == "FM" || a == "MF") || a[0] == a[1]) {
            cout << "ShallowDream" << endl;
            continue;
        }
        if (b == "FM" || b == "MF") {
            cout << "Joker" << endl;
            continue;
        }

        // Sorting based on rank
        sort(a.begin(), a.end(), [&rankMap](char c1, char c2) {
            return getRank(c1, rankMap) > getRank(c2, rankMap);
        });
        sort(b.begin(), b.end(), [&rankMap](char c1, char c2) {
            return getRank(c1, rankMap) > getRank(c2, rankMap);
        });

        // for(auto &aa: a) cout << aa;
        // for(auto &bb: b) cout << bb;

        // Determining the winner
        if (getRank(a[0], rankMap) >= getRank(b[0], rankMap)) {
            cout << "ShallowDream" << endl;
        } else {
            cout << "Joker" << endl;
        }
    }

    return 0;
}
