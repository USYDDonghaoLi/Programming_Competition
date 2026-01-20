class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0 for _ in range(n)]
    
    def fill(self, a):
        for i in range(self.n):
            self.update(i, a[i])

    def lowbit(self, x):
        return x & (-x)

    def update(self, pos, x):
        while pos < self.n:
            self.tree[pos] += x
            pos += self.lowbit(pos)

    def query(self, pos):
        to_ret = 0
        while pos:
            to_ret += self.tree[pos]
            pos -= self.lowbit(pos)
        return to_ret

    def query_sum(self, l, r):
        return self.query(r) - self.query(l - 1)

    def lower_bound(self, val):
        ret, su = 0, 0
        for i in reversed(range(self.n.bit_length())):
            ix = ret + (1 << i)
            if ix < self.n and su + self.tree[ix] < val:
                su += self.tree[ix]
                ret += 1 << i
        return ret
    
    def upper_bound(self, val):
        ret, su = 0, 0
        for i in reversed(range(self.n.bit_length())):
            ix = ret + (1 << i)
            if ix < self.n and su + self.tree[ix] <= val:
                su += self.tree[ix]
                ret += 1 << i
        return ret