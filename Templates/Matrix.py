mod = None

class Matrix:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.mat = [[0] * self.m for _ in range(self.n)]
        self.mod = mod
    
    def build(self, mat):
        '''
        initialize matrix
        '''
        assert len(mat) == self.n and len(mat[0]) == self.m, "Matrix dimensions must agree"
        for i in range(self.n):
            for j in range(self.m):
                self.mat[i][j] = mat[i][j]
        return self
    
    def setMod(self, mod):
        '''
        update mod
        '''
        self.mod = mod
    
    def __getitem__(self, index):
        row, col = index
        return self.mat[row][col]

    def __setitem__(self, index, value):
        row, col = index
        self.mat[row][col] = value
    
    def __iter__(self):
        self.current_col = 0
        self.current_row = 0
        return self
    
    def __next__(self):
        if self.current_row >= self.n:
            raise StopIteration
        value = self.mat[self.current_row][self.current_col]
        self.current_col += 1
        if self.current_col == self.m:
            self.current_row += 1
            self.current_col = 0
        return value

    def build_identity(self, lim):
        '''
        initialize matrix as I
        '''
        for i in range(lim + 1):
            self.mat[i][i] = 1
        return self

    def __mul__(self, other):
        assert self.m == other.n, "Matrix dimensions must agree"
        result = Matrix(self.n, other.m)
        
        if self.mod:
            for i in range(self.n):
                for j in range(other.m):
                    for k in range(self.m):
                        result.mat[i][j] += self.mat[i][k] * other.mat[k][j] % self.mod
                        result.mat[i][j] %= self.mod
        else:
            for i in range(self.n):
                for j in range(other.m):
                    for k in range(self.m):
                        result.mat[i][j] += self.mat[i][k] * other.mat[k][j]
                        
        return result

    def __add__(self, other):
        assert self.n == other.n and self.m == other.m, "Matrix dimensions must agree"
        result = Matrix(self.n, self.m)
        
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
        assert self.n == other.n and self.m == other.m, "Matrix dimensions must agree"
        result = Matrix(self.n, self.m)
        
        if self.mod:
            for i in range(self.n):
                for j in range(self.m):
                    result.mat[i][j] = (self.mat[i][j] - other.mat[i][j]) % self.mod
        else:
            for i in range(self.n):
                for j in range(self.m):
                    result.mat[i][j] = self.mat[i][j] - other.mat[i][j]
                    
        return result

    def qpow_matrix(self, b):
        res = Matrix(self.n, self.n)
        res.build_identity(self.n - 1)
        a = self
        while b:
            if b & 1:
                res = res * a
            a = a * a
            b >>= 1
        return res

    @staticmethod
    def gauss(n, a):
        '''
        find solution of linear equations (float number)
        '''
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
                    '''
                    No Solution
                    '''
                    return 2
            '''
            Infinite solution
            '''
            return 1
        
        for i in range(n - 1, -1, -1):
            for j in range(i + 1, n):
                a[i][n] -= a[i][j] * a[j][n]
        
        '''
        Single solution    
        '''
        return [a[i][-1] for i in range(n)]

    def gauss_jordan(self, n):
        '''
        find solution of linear equtaion (with mod)
        '''
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
                '''
                因为求逆，取两倍
                '''
                for j in range(i, 2 * n):
                    self.mat[k][j] = (self.mat[k][j] - p * self.mat[i][j] % self.mod ) % self.mod
            for j in range(i, 2 * n):
                self.mat[i][j] = self.mat[i][j] * inv % self.mod
        return True

    def get_inv_matrix(self, n):
        '''
        get inverse matrix of current matrix
        '''
        extended_matrix = [row[:] + [1 if i == j else 0 for j in range(self.n)] for i, row in enumerate(self.mat)]
        aug_matrix = Matrix(n, 2 * n)
        aug_matrix.mat = extended_matrix
        if aug_matrix.gauss_jordan(n):
            inv_mat = Matrix(n, n)
            for i in range(n):
                for j in range(n):
                    inv_mat.mat[i][j] = aug_matrix.mat[i][j + n]
            return inv_mat
        else:
            raise ValueError("Matrix is singular and cannot be inverted")
    
    def determinant(self):
        '''
        calculate the determinant of the matrix
        Caution: self.mod must be prime
        '''
        assert self.n == self.m, "Matrix must be square"
        n = self.n
        mat_copy = [row[:] for row in self.mat]
        det = 1
        for i in range(n):
            pivot = i
            for j in range(i + 1, n):
                if abs(mat_copy[j][i]) > abs(mat_copy[pivot][i]):
                    pivot = j
            if i != pivot:
                mat_copy[i], mat_copy[pivot] = mat_copy[pivot], mat_copy[i]
                det = -det
            if mat_copy[i][i] == 0:
                return 0
            det = det * mat_copy[i][i] % self.mod
            inv = pow(mat_copy[i][i], self.mod - 2, self.mod)
            assert inv * mat_copy[i][i] % self.mod == 1
            for j in range(i + 1, n):
                factor = mat_copy[j][i] * inv % self.mod
                for k in range(i, n):
                    mat_copy[j][k] = (mat_copy[j][k] - factor * mat_copy[i][k] % self.mod) % self.mod
        return det % self.mod

    def Determinant(self):
        '''
        calculate the determinant of the matrix for any mod
        '''
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
        # res, w = 1, 1
        
        # for i in range(self.n):
        #     for j in range(i + 1, self.n):
        #         while self.mat[i][i]:
        #             div = self.mat[j][i] // self.mat[i][i]
        #             for k in range(i, self.n):
        #                 self.mat[j][k] -= div * self.mat[i][k] % self.mod
        #                 self.mat[j][k] %= self.mod
        #             self.mat[i], self.mat[j] = self.mat[j], self.mat[i]
        #             w = -w
        #         self.mat[i], self.mat[j] = self.mat[j], self.mat[i]
        #         w = -w

        # for i in range(self.n):
        #     res = self.mat[i][i] * res % self.mod
        
        # return w * res % self.mod

    def __str__(self):
        res = []
        for i in range(self.n):
            res.append(" ".join(map(str, self.mat[i])))
        return "\n".join(res)