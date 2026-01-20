class Hash:
    def __init__(self, arr) -> None:
        if arr[0].isalpha():
            self.arr = [ord(c) for c in arr]
        else:
            self.arr = arr
        self.mul = 131
        self.mod = 10 ** 9 + 7
        self.n = len(arr)
        self.mulpw = [1 for _ in range(self.n + 1)]
        for i in range(1, self.n + 1):
            self.mulpw[i] = self.mulpw[i - 1] * self.mul % self.mod

        self.HASH = [0]
        for c in self.arr:
            self.HASH.append((self.HASH[-1] * self.mul + c) % self.mod)

    #[l, r)
    def GetHash(self, l, r):
        return (self.HASH[r] - self.HASH[l] * self.mulpw[r - l]) % self.mod

    #[l, r]
    def CheckEqual(self, start, end, sz):
        pattern = self.GetHash(0, sz)
        for i in range(start, end - sz + 2, sz):
            if self.GetHash(i, i + sz) != pattern:
                return False
        return True
    
    #[l, r)
    def Check(self, ls, le, rs, re):
        return self.GetHash(ls, le) == self.GetHash(rs, re)
    
    @staticmethod
    def calc(arr):
        if arr[0].isalpha():
            arr = [ord(c) for c in arr]
        else:
            pass
        mul = 131
        mod = 10 ** 9 + 7
        n = len(arr)
        res = 0
        
        for c in arr:
            res = (res * mul + c) % mod
        
        return res