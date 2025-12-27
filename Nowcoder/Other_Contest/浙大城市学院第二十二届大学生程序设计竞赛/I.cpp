#include <iostream>
#include <vector>
#include <queue>

using namespace std;

const int N = 4000010;

struct nd {
    int len, link, cnt;
    int tr[26];
} nodes[N];
int nc = 0;
int vis[N];
int ts = 0;

int cr() {
    memset(nodes[nc].tr, -1, sizeof(nodes[nc].tr));
    nodes[nc].len = 0;
    nodes[nc].link = -1;
    nodes[nc].cnt = 0;
    return nc++;
}

int rt;

vector<int> ins(const vector<char>& s) {
    vector<int> terms;
    int lst = rt;
    for (char ch : s) {
        int c = ch - 'a';
        int p = lst;
        if (nodes[p].tr[c] != -1) {
            int q = nodes[p].tr[c];
            if (nodes[q].len == nodes[p].len + 1) {
                lst = q;
            } else {
                int cl = cr();
                nodes[cl].len = nodes[p].len + 1;
                nodes[cl].link = nodes[q].link;
                memcpy(nodes[cl].tr, nodes[q].tr, sizeof(nodes[q].tr));
                nodes[cl].cnt = nodes[q].cnt;
                nodes[q].link = cl;
                lst = cl;
                for (; p != -1 && nodes[p].tr[c] == q; p = nodes[p].link) {
                    nodes[p].tr[c] = cl;
                }
            }
        } else {
            int u = cr();
            nodes[u].len = nodes[p].len + 1;
            lst = u;
            int pp = p;
            while (pp != -1 && nodes[pp].tr[c] == -1) {
                nodes[pp].tr[c] = u;
                pp = nodes[pp].link;
            }
            if (pp == -1) {
                nodes[u].link = rt;
            } else {
                int q = nodes[pp].tr[c];
                if (nodes[pp].len + 1 == nodes[q].len) {
                    nodes[u].link = q;
                } else {
                    int cl = cr();
                    nodes[cl].len = nodes[pp].len + 1;
                    memcpy(nodes[cl].tr, nodes[q].tr, sizeof(nodes[q].tr));
                    nodes[cl].link = nodes[q].link;
                    nodes[cl].cnt = nodes[q].cnt;
                    nodes[q].link = cl;
                    nodes[u].link = cl;
                    for (; pp != -1 && nodes[pp].tr[c] == q; pp = nodes[pp].link) {
                        nodes[pp].tr[c] = cl;
                    }
                }
            }
        }
        terms.push_back(lst);
    }
    return terms;
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    string ini;
    cin >> ini;
    vector<char> S(ini.begin(), ini.end());
    rt = cr();
    int tv = 0;
    long long ans = 0;
    auto terms = ins(S);
    int ot = tv;
    tv++;
    long long na = 0;
    ts++;
    queue<int> qq;
    for (int t : terms) {
        if (vis[t] != ts) {
            vis[t] = ts;
            qq.push(t);
        }
    }
    while (!qq.empty()) {
        int p = qq.front(); qq.pop();
        if (nodes[p].cnt == ot) {
            int lk = nodes[p].link;
            int pl = (lk == -1 ? 0 : nodes[lk].len);
            na += nodes[p].len - pl;
        }
        nodes[p].cnt++;
        int lk = nodes[p].link;
        if (lk != -1 && vis[lk] != ts) {
            vis[lk] = ts;
            qq.push(lk);
        }
    }
    ans = na;
    int q;
    cin >> q;
    for (int i = 0; i < q; i++) {
        string op;
        cin >> op;
        if (op == "I") {
            int pos;
            char c;
            cin >> pos >> c;
            S.insert(S.begin() + pos, c);
            terms = ins(S);
            ot = tv;
            tv++;
            na = 0;
            ts++;
            qq = queue<int>();
            for (int t : terms) {
                if (vis[t] != ts) {
                    vis[t] = ts;
                    qq.push(t);
                }
            }
            while (!qq.empty()) {
                int p = qq.front(); qq.pop();
                if (nodes[p].cnt == ot) {
                    int lk = nodes[p].link;
                    int pl = (lk == -1 ? 0 : nodes[lk].len);
                    na += nodes[p].len - pl;
                }
                nodes[p].cnt++;
                int lk = nodes[p].link;
                if (lk != -1 && vis[lk] != ts) {
                    vis[lk] = ts;
                    qq.push(lk);
                }
            }
            ans = na;
        } else if (op == "D") {
            int pos;
            cin >> pos;
            S.erase(S.begin() + pos);
            terms = ins(S);
            ot = tv;
            tv++;
            na = 0;
            ts++;
            qq = queue<int>();
            for (int t : terms) {
                if (vis[t] != ts) {
                    vis[t] = ts;
                    qq.push(t);
                }
            }
            while (!qq.empty()) {
                int p = qq.front(); qq.pop();
                if (nodes[p].cnt == ot) {
                    int lk = nodes[p].link;
                    int pl = (lk == -1 ? 0 : nodes[lk].len);
                    na += nodes[p].len - pl;
                }
                nodes[p].cnt++;
                int lk = nodes[p].link;
                if (lk != -1 && vis[lk] != ts) {
                    vis[lk] = ts;
                    qq.push(lk);
                }
            }
            ans = na;
        } else if (op == "Q") {
            cout << ans << "\n";
        }
    }
    return 0;
}