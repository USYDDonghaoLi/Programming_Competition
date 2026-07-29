#include <iostream>
#include <algorithm>
using namespace std;

using ll = long long;

pair<int, int> get_eo(int L, int R) {
    if (L > R) return {0, 0};
    int tot = R - L + 1;
    if (L % 2 == 0) {
        return {(tot + 1) / 2, tot / 2};
    } else {
        return {tot / 2, (tot + 1) / 2};
    }
}

struct Node {
    Node *l, *r;
    int e1, o1;
    int assign; // -1: none, 0/1: assign value
    int flip;
    Node() : l(nullptr), r(nullptr), e1(0), o1(0), assign(-1), flip(0) {}
};

void apply(Node* node, int L, int R, int ass, int flp) {
    if (ass != -1) {
        auto [e, o] = get_eo(L, R);
        node->e1 = ass ? e : 0;
        node->o1 = ass ? o : 0;
        node->assign = ass;
        node->flip = 0;
    }
    if (flp) {
        auto [e, o] = get_eo(L, R);
        node->e1 = e - node->e1;
        node->o1 = o - node->o1;
        if (node->assign != -1) {
            node->assign ^= 1;
        } else {
            node->flip ^= 1;
        }
    }
}

void push(Node* node, int L, int R) {
    if (node->assign == -1 && node->flip == 0) return;
    int mid = (L + R) >> 1;
    if (!node->l) node->l = new Node();
    if (!node->r) node->r = new Node();
    apply(node->l, L, mid, node->assign, node->flip);
    apply(node->r, mid + 1, R, node->assign, node->flip);
    node->assign = -1;
    node->flip = 0;
}

void pull(Node* node) {
    node->e1 = (node->l ? node->l->e1 : 0) + (node->r ? node->r->e1 : 0);
    node->o1 = (node->l ? node->l->o1 : 0) + (node->r ? node->r->o1 : 0);
}

void upd_ass(Node* node, int L, int R, int ql, int qr, int val) {
    if (R < ql || L > qr) return;
    if (ql <= L && R <= qr) {
        apply(node, L, R, val, 0);
        return;
    }
    if (!node->l) node->l = new Node();
    if (!node->r) node->r = new Node();
    push(node, L, R);
    int mid = (L + R) >> 1;
    upd_ass(node->l, L, mid, ql, qr, val);
    upd_ass(node->r, mid + 1, R, ql, qr, val);
    pull(node);
}

void upd_flp(Node* node, int L, int R, int ql, int qr) {
    if (R < ql || L > qr) return;
    if (ql <= L && R <= qr) {
        apply(node, L, R, -1, 1);
        return;
    }
    if (!node->l) node->l = new Node();
    if (!node->r) node->r = new Node();
    push(node, L, R);
    int mid = (L + R) >> 1;
    upd_flp(node->l, L, mid, ql, qr);
    upd_flp(node->r, mid + 1, R, ql, qr);
    pull(node);
}

pair<int, int> qry(Node* node, int L, int R, int ql, int qr) {
    if (!node || R < ql || L > qr) return {0, 0};
    if (ql <= L && R <= qr) return {node->e1, node->o1};
    if (node->assign != -1 || node->flip) {
        push(node, L, R);
    }
    int mid = (L + R) >> 1;
    auto [e1, o1] = qry(node->l, L, mid, ql, qr);
    auto [e2, o2] = qry(node->r, mid + 1, R, ql, qr);
    return {e1 + e2, o1 + o2};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    Node* root = new Node();

    while (q--) {
        int op, l, r;
        cin >> op >> l >> r;
        if (op == 1) {
            upd_ass(root, 1, n, l, r, 1);
        } else if (op == 2) {
            upd_flp(root, 1, n, l, r);
        } else {
            auto [e1, o1] = qry(root, 1, n, l, r);
            auto [E, O] = get_eo(l, r);
            cout << min(e1 + O - o1, E - e1 + o1) << '\n';
        }
    }
    return 0;
}