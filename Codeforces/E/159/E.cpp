#include <bits/stdc++.h>
using namespace std;

class TrieNode {
public:
    unordered_map<char, TrieNode*> children;
    int cnt;

    TrieNode() : cnt(0) {}
};

class Trie {
private:
    TrieNode* root;

public:
    Trie() {
        root = new TrieNode();
    }

    void insert(const string &word) {
        TrieNode* node = root;
        node->cnt++;
        for (char ch : word) {
            if (node->children.find(ch) == node->children.end()) {
                node->children[ch] = new TrieNode();
            }
            node = node->children[ch];
            node->cnt++;
        }
    }

    int calc(const string &word) {
        int res = 0;
        TrieNode* node = root;

        for (char ch : word) {
            if (node->children.find(ch) == node->children.end()) {
                break;
            }
            node = node->children[ch];
            res += node->cnt;
        }

        return res;
    }
};

void solve() {
    int n;
    cin >> n;
    vector<string> words(n);
    for (int i = 0; i < n; ++i) {
        cin >> words[i]; 
    }

    Trie T;
    long long res = 0;
    for (const string &word : words) {
        T.insert(word);
        res += 2LL * n * word.length();
    }

    for (const string &word : words) {
        string rev_word = word;
        reverse(rev_word.begin(), rev_word.end());
        res -= 2 * T.calc(rev_word);
    }

    cout << res << endl;
}

int main() {
    int t = 1; // Change if there are multiple test cases
    while (t--) {
        solve();
    }
    return 0;
}
