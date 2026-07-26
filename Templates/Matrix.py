class Matrix:
    """
    矩阵模板，支持基本运算、幂运算、高斯消元、行列式、逆矩阵等。
    支持取模和不取模两种情况。
    """

    def __init__(self, n, m, mod=None):
        """
        初始化矩阵。
        Args:
            n: 行数
            m: 列数
            mod: 取模数，如果为 None 则不取模
        """
        self.n = n
        self.m = m
        self.mat = [[0] * self.m for _ in range(self.n)]
        self.mod = mod
    def build(self, mat):
        """初始化矩阵值。"""
        assert len(mat) == self.n and len(mat[0]) == self.m, "Matrix dimensions must agree"
        for i in range(self.n):
            for j in range(self.m):
                self.mat[i][j] = mat[i][j]
        return self

    def set_mod(self, mod):
        """设置取模数。"""
        self.mod = mod
        return self

    def copy(self):
        """返回当前矩阵的深拷贝。"""
        new_mat = Matrix(self.n, self.m, self.mod)
        for i in range(self.n):
            for j in range(self.m):
                new_mat.mat[i][j] = self.mat[i][j]
        return new_mat

    def transpose(self):
        """返回转置矩阵。"""
        new_mat = Matrix(self.m, self.n, self.mod)
        for i in range(self.n):
            for j in range(self.m):
                new_mat.mat[j][i] = self.mat[i][j]
        return new_mat
    
    def __getitem__(self, index):
        row, col = index
        return self.mat[row][col]

    def __setitem__(self, index, value):
        row, col = index
        self.mat[row][col] = value

    def __iter__(self):
        """迭代矩阵中所有元素（按行序）。"""
        for i in range(self.n):
            for j in range(self.m):
                yield self.mat[i][j]

    def build_identity(self, lim):
        """初始化为单位矩阵。"""
        for i in range(lim + 1):
            self.mat[i][i] = 1
        return self

    def __mul__(self, other):
        """矩阵乘法。"""
        assert self.m == other.n, "Matrix dimensions must agree"
        result = Matrix(self.n, other.m, self.mod)

        if self.mod:
            for i in range(self.n):
                for j in range(other.m):
                    for k in range(self.m):
                        result.mat[i][j] += self.mat[i][k] * other.mat[k][j]
                        result.mat[i][j] %= self.mod
        else:
            for i in range(self.n):
                for j in range(other.m):
                    for k in range(self.m):
                        result.mat[i][j] += self.mat[i][k] * other.mat[k][j]

        return result

    def __add__(self, other):
        """矩阵加法。"""
        assert self.n == other.n and self.m == other.m, "Matrix dimensions must agree"
        result = Matrix(self.n, self.m, self.mod)

        if self.mod:
            for i in range(self.n):
                for j in range(self.m):
                    result.mat[i][j] = (self.mat[i][j] + other.mat[i][j]) % self.mod
        else:
            for i in range(self.n):
                for j in range(self.m):
                    result.mat[i][j] = self.mat[i][j] + other.mat[i][j]

        return result

    def __sub__(self, other):
        """矩阵减法。"""
        assert self.n == other.n and self.m == other.m, "Matrix dimensions must agree"
        result = Matrix(self.n, self.m, self.mod)

        if self.mod:
            for i in range(self.n):
                for j in range(self.m):
                    result.mat[i][j] = (self.mat[i][j] - other.mat[i][j]) % self.mod
        else:
            for i in range(self.n):
                for j in range(self.m):
                    result.mat[i][j] = self.mat[i][j] - other.mat[i][j]

        return result

    def matrix_power(self, b):
        """矩阵快速幂。"""
        assert self.n == self.m, "Matrix must be square"
        res = Matrix(self.n, self.n, self.mod)
        res.build_identity(self.n - 1)
        a = self.copy()
        while b:
            if b & 1:
                res = res * a
            a = a * a
            b >>= 1
        return res

    @staticmethod
    def gauss_float(n, a):
        """
        高斯消元（浮点数）。求解线性方程组。
        Args:
            n: 方程个数
            a: 增广矩阵（最后一列是常数项），二维列表
        Returns:
            返回值含义：
            - 2: 无解
            - 1: 无穷多解
            - 列表: 唯一解 [x0, x1, ..., x_{n-1}]
        """
        eps = 1e-8
        c, r = 0, 0
        for c in range(n):
            cur = r
            for j in range(r + 1, n):
                if abs(a[j][c]) > abs(a[cur][c]):
                    cur = j
            if abs(a[cur][c]) < eps:
                continue
            a[r], a[cur] = a[cur], a[r]
            for i in range(n, c - 1, -1):
                a[r][i] /= a[r][c]
            for i in range(r + 1, n):
                if abs(a[i][c]) > eps:
                    for j in range(n, c - 1, -1):
                        a[i][j] -= a[r][j] * a[i][c]
            r += 1
        if r < n:
            for i in range(r, n):
                if abs(a[i][n]) > eps:
                    return 2
            return 1

        for i in range(n - 1, -1, -1):
            for j in range(i + 1, n):
                a[i][n] -= a[i][j] * a[j][n]

        return [a[i][-1] for i in range(n)]

    def gauss_jordan_mod(self, n):
        """
        高斯-约当消元（模运算下）。求解线性方程组。
        前提：self.mod 必须是素数。
        Args:
            n: 方程个数
        Returns:
            True 表示有解，False 表示无解
        """
        for i in range(n):
            r = i
            for j in range(i + 1, n):
                if self.mat[j][i] > self.mat[r][i]:
                    r = j
            if r != i:
                self.mat[i], self.mat[r] = self.mat[r], self.mat[i]
            if not self.mat[i][i]:
                return False
            inv = pow(self.mat[i][i], self.mod - 2, self.mod)
            for k in range(n):
                if k == i:
                    continue
                p = self.mat[k][i] * inv % self.mod
                for j in range(i, 2 * n):
                    self.mat[k][j] = (self.mat[k][j] - p * self.mat[i][j] % self.mod) % self.mod
            for j in range(i, 2 * n):
                self.mat[i][j] = self.mat[i][j] * inv % self.mod
        return True

    def get_inverse_mod(self, n):
        """
        求逆矩阵（模运算下）。
        前提：self.mod 必须是素数。
        Args:
            n: 矩阵大小
        Returns:
            逆矩阵
        """
        extended_matrix = [row[:] + [1 if i == j else 0 for j in range(self.n)] for i, row in enumerate(self.mat)]
        aug_matrix = Matrix(n, 2 * n, self.mod)
        aug_matrix.mat = extended_matrix
        if aug_matrix.gauss_jordan_mod(n):
            inv_mat = Matrix(n, n, self.mod)
            for i in range(n):
                for j in range(n):
                    inv_mat.mat[i][j] = aug_matrix.mat[i][j + n]
            return inv_mat
        else:
            raise ValueError("Matrix is singular and cannot be inverted")
    
    def determinant_float(self):
        """
        计算行列式（浮点数）。
        """
        assert self.n == self.m, "Matrix must be square"
        n = self.n
        mat_copy = [row[:] for row in self.mat]
        det = 1.0
        eps = 1e-8

        for i in range(n):
            pivot = i
            for j in range(i + 1, n):
                if abs(mat_copy[j][i]) > abs(mat_copy[pivot][i]):
                    pivot = j
            if abs(mat_copy[pivot][i]) < eps:
                return 0
            if i != pivot:
                mat_copy[i], mat_copy[pivot] = mat_copy[pivot], mat_copy[i]
                det = -det
            det *= mat_copy[i][i]
            for j in range(i + 1, n):
                factor = mat_copy[j][i] / mat_copy[i][i]
                for k in range(i, n):
                    mat_copy[j][k] -= factor * mat_copy[i][k]
        return det

    def determinant_mod(self):
        """
        计算行列式（模运算下）。
        前提：self.mod 必须是素数。
        """
        assert self.n == self.m, "Matrix must be square"
        assert self.mod is not None, "mod must be set"
        n = self.n
        mat_copy = [row[:] for row in self.mat]
        det = 1

        for i in range(n):
            pivot = i
            for j in range(i + 1, n):
                if mat_copy[j][i] % self.mod != 0:
                    pivot = j
                    break
            if mat_copy[pivot][i] % self.mod == 0:
                return 0
            if i != pivot:
                mat_copy[i], mat_copy[pivot] = mat_copy[pivot], mat_copy[i]
                det = -det % self.mod
            det = det * mat_copy[i][i] % self.mod
            inv = pow(mat_copy[i][i], self.mod - 2, self.mod)
            for j in range(i + 1, n):
                factor = mat_copy[j][i] * inv % self.mod
                for k in range(i, n):
                    mat_copy[j][k] = (mat_copy[j][k] - factor * mat_copy[i][k] % self.mod) % self.mod
        return det % self.mod

    def determinant_general_mod(self):
        """
        计算行列式（模运算下，不需要 mod 是素数）。
        使用辗转相除法。
        """
        assert self.n == self.m, "Matrix must be square"
        assert self.mod is not None, "mod must be set"
        res = 1
        for c in range(self.n):
            for r in range(c + 1, self.n):
                while self.mat[r][c]:
                    self.mat[r], self.mat[c] = self.mat[c], self.mat[r]
                    res *= -1
                    if not self.mat[r][c]:
                        break
                    if self.mat[r][c] >= self.mat[c][c]:
                        div = self.mat[r][c] // self.mat[c][c]
                        for k in range(c, self.n):
                            self.mat[r][k] = (self.mat[r][k] - div * self.mat[c][k]) % self.mod
                    if not self.mat[r][c]:
                        break

        for i in range(self.n):
            res = res * self.mat[i][i] % self.mod

        return res

    def __str__(self):
        res = []
        for i in range(self.n):
            res.append(" ".join(map(str, self.mat[i])))
        return "\n".join(res)