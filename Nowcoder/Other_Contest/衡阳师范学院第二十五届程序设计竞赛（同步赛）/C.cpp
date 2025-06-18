#include <bits/stdc++.h>
using namespace std;
using i64 = long long;
const int N = 5e5 + 5;
const i64 MOF = 0x3f3f3f3f3f3f3f3f;
i64 x, y;
i64 a[N + 1][2], b[4][N + 1];
struct Segtree{
	int siz;
	i64 lzy;
	i64 l[4], r[4];
	i64 mx[4], mn[4];
	i64 co_mx1, co_mn1;
	i64 co_mx2, co_mn2;
	Segtree(int siz = 0, i64 lzy = 0, i64 co_mx1 = 0, i64 co_mn1 = MOF, i64 co_mx2 = 0, i64 co_mn2 = MOF)
	: siz(siz), lzy(lzy), co_mx1(co_mx1), co_mn1(co_mn1), co_mx2(co_mx2), co_mn2(co_mn2) {
		for (int i = 0; i < 4; i++) {
			l[i] = r[i] = 0;
			mx[i] = -MOF;
			mn[i] = MOF;
		}
	}
	#define ls (root << 1)
	#define rs (root << 1 | 1)
	#define rt_ tree[root]
	#define ls_ tree[ls]
	#define rs_ tree[rs]
};

Segtree tree[N << 2];
inline Segtree hb(Segtree &_i, Segtree &_j) {
	Segtree k = Segtree();
	k.siz = _i.siz + _j.siz;
	if (k.siz == 0) return k;
	if (_i.siz == 0) return _j;
	if (_j.siz == 0) return _i;
	i64 mxx1 = 0, mxx2 = 0;
	for (int i = 0; i < 4; i++) {
		k.l[i] = _i.l[i];
		k.r[i] = _j.r[i];
		k.mx[i] = max(_i.mx[i], _j.mx[i]);
		k.mn[i] = min(_i.mn[i], _j.mn[i]);
		mxx1 = max(mxx1, abs(_i.r[i] - _j.l[i]));
		if (i == 1 || i == 2) mxx2 = max(mxx2, abs(_i.r[i] - _j.l[i]));
	}
	k.co_mx1 = max({_i.co_mx1, _j.co_mx1, mxx1});
	k.co_mn1 = min({_i.co_mn1, _j.co_mn1, mxx1});
	k.co_mx2 = max({_i.co_mx2, _j.co_mx2, mxx2});
	k.co_mn2 = min({_i.co_mn2, _j.co_mn2, mxx2});
	return k;
}

inline void push_up(int root) {
	tree[root] = hb(tree[ls], tree[rs]);
}

inline void build(int root, int l, int r) {
	if (l == r) {
		tree[root].siz = 1;
		for (int i = 0; i < 4; i++) {
			rt_.l[i] = b[i][l];
			rt_.r[i] = b[i][l];
			rt_.mx[i] = b[i][l];
			rt_.mn[i] = b[i][l];
		}
		return;
	}
	int mid = l + r >> 1;
	build(ls, l, mid);
	build(rs, mid + 1, r);
	push_up(root);
}

inline void push_mark(int root, int l, int r) {
	if (tree[root].lzy) {
		i64 sum = powl(2, tree[root].lzy);
		ls_.lzy += rt_.lzy;
		rs_.lzy += rt_.lzy;
		rt_.lzy = 0;
		for (int i = 0; i < 4; i++) {
			if (i == 0 || i == 3) {
				ls_.l[i] = rs_.l[i] = 0;
				ls_.r[i] = rs_.r[i] = 0;
				ls_.mx[i] = rs_.mx[i] = 0;
				ls_.mn[i] = rs_.mn[i] = 0;
			} else {
				ls_.l[i] *= sum;
				rs_.l[i] *= sum;
				ls_.r[i] *= sum;
				rs_.r[i] *= sum;
				ls_.mx[i] *= sum;
				rs_.mx[i] *= sum;
				ls_.mn[i] *= sum;
				rs_.mn[i] *= sum;
			}
		}
		if (ls_.siz != 1) {
			ls_.co_mx2 *= sum;
			ls_.co_mn2 *= sum;
			ls_.co_mx1 = ls_.co_mx2;
			ls_.co_mn1 = ls_.co_mn2;
		}
		if (rs_.siz != 1) {
			rs_.co_mx2 *= sum;
			rs_.co_mn2 *= sum;
			rs_.co_mx1 = rs_.co_mx2;
			rs_.co_mn1 = rs_.co_mn2;
			
		}
	}
}

inline void update(int root, int l, int r, int ql, int qr, int op) {
	if (r < ql || l > qr) return;
	if (l >= ql && r <= qr) {
		if (op == 1) {
			b[0][l] = x + y;
			b[1][l] = x - y;
			b[2][l] = y - x;
			b[3][l] = -(x + y);
			for (int i = 0; i < 4; i++) {
				rt_.l[i] = b[i][l];
				rt_.r[i] = b[i][l];
				rt_.mx[i] = b[i][l];
				rt_.mn[i] = b[i][l];
			}
		} else {
			rt_.lzy++;
			for (int i = 0; i < 4; i++) {
				if (i == 0 || i == 3) {
					rt_.l[i] = rt_.r[i] = 0;
					rt_.mx[i] = rt_.mn[i] = 0;
				} else {
					rt_.l[i] <<= 1;
					rt_.r[i] <<= 1;
					rt_.mx[i] <<= 1;
					rt_.mn[i] <<= 1;
				}
			}
			if (l != r) {
				rt_.co_mx2 <<= 1;
				rt_.co_mn2 <<= 1;
				rt_.co_mx1 = rt_.co_mx2;
				rt_.co_mn1 = rt_.co_mn2;
			}
		}
		return;
	}
	push_mark(root, l, r);
	int mid = l + r >> 1;
	update(ls, l, mid, ql, qr, op);
	update(rs, mid + 1, r, ql, qr, op);
	push_up(root);
}

inline Segtree query(int root, int l, int r, int &ql, int &qr) {
	if (r < ql || l > qr) return Segtree();
	if (l >= ql && r <= qr) return rt_;
	push_mark(root, l, r);
	int mid = l + r >> 1;
	auto LS = query(ls, l, mid, ql, qr), RS = query(rs, mid + 1, r, ql, qr);
	return hb(LS, RS);
}

void solve() {
	int n, m; cin >> n >> m;
	for (int i = 1; i <= n; i++) {
		cin >> x >> y;
		a[i][0] = x, a[i][1] = y;
		b[0][i] = x + y;
		b[1][i] = x - y;
		b[2][i] = y - x;
		b[3][i] = -(x + y);
	}
	build(1, 1, n);
	for (int i = 1; i <= m; i++) {
		int op; cin >> op;
		if (op == 0) {
			int l, r; cin >> l >> r;
			update(1, 1, n, l, r, op);
		} else if (op == 1) {
			int pos; cin >> pos >> x >> y;
			update(1, 1, n, pos, pos, op);
		} else if (op == 2) {
			int l, r; cin >> l >> r;
			auto ans = query(1, 1, n, l, r);
			i64 mx = 0;
			for (int i = 0; i < 4; i++) mx = max(mx, ans.mx[i] - ans.mn[i]);
			cout << mx << '\n';
		} else if (op == 3) {
			int l, r; cin >> l >> r;
			auto ans = query(1, 1, n, l, r);
			i64 sum1 = ans.co_mx1, sum2 = ans.co_mn1;
			cout << sum1 - sum2 << '\n';
		} else if (op == 4) {
			int l;
			i64 k; cin >> l >> k;
			int L = l + 1, R = n;
			while (L < R) {
				int mid = L + R >> 1;
				i64 ans = -MOF;
				auto d = query(1, 1, n, l, mid);
				for (int i = 0; i < 4; i++) ans = max(ans, d.mx[i] - d.mn[i]);
				if (ans <= k) L = mid + 1;
				else R = mid;
			}
			i64 ans = -MOF;
			if (L > n) {
				cout << "-1\n";
				continue;
			}
			auto d = query(1, 1, n, l, L);
			for (int i = 0; i < 4; i++) ans = max(ans, d.mx[i] - d.mn[i]);
			if (ans > k) cout << L - l + 1 << '\n';
			else cout << "-1\n";
		}
	}
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0), cout.tie(0);
    int _ = 1;
    // std::cin >> _;
    while (_--) {
        solve();
    }
    return 0;
}
