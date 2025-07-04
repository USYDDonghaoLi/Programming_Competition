#include <bits/stdc++.h>
using namespace std;

const int MOD = 998244353;

struct Matrix {
    int mat[3][3];

    Matrix() {
        memset(mat, 0, sizeof(mat));
    }

    static Matrix identity() {
        Matrix result;
        for (int i = 0; i < 3; ++i) {
            result.mat[i][i] = 1;
        }
        return result;
    }

    Matrix operator+(const Matrix &other) const {
        Matrix result;
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; ++j) {
                result.mat[i][j] = (mat[i][j] + other.mat[i][j]) % MOD;
            }
        }
        return result;
    }

    Matrix operator*(const Matrix &other) const {
        Matrix result;
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; ++j) {
                for (int k = 0; k < 3; ++k) {
                    result.mat[i][j] = (result.mat[i][j] + 1LL * mat[i][k] * other.mat[k][j] % MOD) % MOD;
                }
            }
        }
        return result;
    }

    bool operator!=(const Matrix &other) const {
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; ++j) {
                if (mat[i][j] != other.mat[i][j]) {
                    return true;
                }
            }
        }
        return false;
    }
};

Matrix getMatrix(int a) {
    Matrix res;
    res.mat[a][a] = 1;
    return res;
}

Matrix getSwap(int a, int b) {
    Matrix res = Matrix::identity();
    swap(res.mat[a][a], res.mat[a][b]);
    swap(res.mat[b][a], res.mat[b][b]);
    return res;
}

Matrix getAdd(int a, int b) {
    Matrix res = Matrix::identity();
    swap(res.mat[a][a], res.mat[a][b]);
    return res;
}

Matrix getMul(int a) {
    Matrix res = Matrix::identity();
    res.mat[a][a] = 2;
    return res;
}


class LazySegmentTree {
private:
    vector<Matrix> tree, lazy;
    int n;

    void build(const vector<int> &nums, int v, int tl, int tr) {
        if (tl == tr) {
            tree[v] = getMatrix(nums[tl]);
        } else {
            int tm = (tl + tr) / 2;
            build(nums, v*2, tl, tm);
            build(nums, v*2+1, tm+1, tr);
            tree[v] = tree[v*2] + tree[v*2+1];
        }
    }

    void push(int v, int tl, int tr) {
        if (lazy[v] != Matrix::identity()) {
            tree[v] = tree[v] * lazy[v];
            if (tl != tr) {
                lazy[v*2] = lazy[v*2] * lazy[v];
                lazy[v*2+1] = lazy[v*2+1] * lazy[v];
            }
            lazy[v] = Matrix::identity();
        }
    }

    void update(int v, int tl, int tr, int l, int r, const Matrix &new_val) {
        push(v, tl, tr);
        if (l > r) return;
        if (l == tl && r == tr) {
            lazy[v] = new_val;
            push(v, tl, tr);
        } else {
            int tm = (tl + tr) / 2;
            update(v*2, tl, tm, l, min(r, tm), new_val);
            update(v*2+1, tm+1, tr, max(l, tm+1), r, new_val);
            tree[v] = tree[v*2] + tree[v*2+1];
        }
    }

    Matrix query(int v, int tl, int tr, int l, int r) {
        if (l > r) return Matrix(); // return empty matrix
        push(v, tl, tr);
        if (l == tl && r == tr) {
            return tree[v];
        }
        int tm = (tl + tr) / 2;
        return query(v*2, tl, tm, l, min(r, tm)) + query(v*2+1, tm+1, tr, max(l, tm+1), r);
    }

public:
    LazySegmentTree(const vector<int> &nums) {
        n = nums.size();
        tree.resize(n * 4);
        lazy.assign(n * 4, Matrix::identity());
        build(nums, 1, 0, n - 1);
    }

    void update(int l, int r, const Matrix &new_val) {
        update(1, 0, n - 1, l, r, new_val);
    }

    Matrix query(int l, int r) {
        return query(1, 0, n - 1, l, r);
    }

    // Implement other methods like getMatrix, etc., based on the Python code logic.
};

void solve() {
    int n, m;
    cin >> n >> m;
    vector<int> nums(n);
    for (int &num : nums) {
        cin >> num;
        --num;
    }

    LazySegmentTree segTree(nums);

    for (int i = 0; i < m; ++i){
        int l, r, op, a, b;
        cin >> l >> r >> op;
        --l;
        --r;

        if (op == 1){
            cin >> a >> b;
            --a;
            --b;
            Matrix tmp = getSwap(a, b);
            segTree.update(l, r, tmp);
        }
        else if (op == 2){
            cin >> a >> b;
            --a;
            --b;
            Matrix tmp = getAdd(a, b);
            segTree.update(l, r, tmp);
        }
        else{
            cin >> a;
            --a;
            Matrix tmp = getMul(a);
            segTree.update(l, r, tmp);
        }

        vector<int> res(3, 0);
        Matrix tmp = segTree.query(0, n - 1);
        for (int i = 0; i < 3; i++){
            for (int j = 0; j < 3; j++){
                res[j] += tmp.mat[i][j];
                res[j] %= MOD;
            }
        }
        for (int i = 0; i < 3; i++){
            cout << res[i] << " \n"[i == 2];
        }
    }
    // Implement the logic for processing the operations as in Python code.
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
