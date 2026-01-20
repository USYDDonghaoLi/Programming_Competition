#f(a, a) = a#
class SpraseTable:
    def __init__(self, v, op, e) -> None:
        self.n = len(v)
        self.op = op
        self.e = e
        self.v = v
        self.l = (self.n).bit_length()
        self.info=[[e for _ in range(self.l)] for _ in range(self.n)]
        for i in range(self.n):
            self.info[i][0] = self.v[i]
        
        for i in range(1, self.l):
            for j in range(self.n):
                if j + (1 << i) - 1 < self.n:
                    self.info[j][i] = self.op(self.info[j][i - 1], self.info[j + (1 << (i - 1))][i - 1])
    
        self.log2 = [-1 for _ in range(self.n + 1)]
        self.log2[1] = 0
        for i in range(2, self.n + 1):
            self.log2[i] = self.log2[i >> 1] + 1
    
    def query(self, l, r):
        s = self.log2[r - l + 1]
        return self.op(self.info[l][s], self.info[r - (1 << s) + 1][s])