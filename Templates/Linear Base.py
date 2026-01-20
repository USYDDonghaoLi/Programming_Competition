class LinearBase:

    def __init__(self, nums) -> None:
        self.bases = []
        self.n = len(nums)
        for num in nums:
            tot = len(self.bases)
            for i in range(tot):
                num = min(num, num ^ self.bases[i])
            if num:
                for i in range(tot):
                    self.bases[i] = min(self.bases[i], self.bases[i] ^ num)
                self.bases.append(num)
        self.bases.sort()
    
    def kthlargestxor(self, k):
        ans = 0
        '''
        判断有没有可能异或出0
        '''
        # if len(self.bases) < self.n or some request:
        #     k -= 1
        k -= 1
        for base in self.bases:
            if k & 1:
                ans ^= base
            k >>= 1
        
        if k == 0:
            return ans
        else:
            return -1

class LinearBase2:

    def __init__(self, n) -> None:
        self.n = n
        self.base = [0 for _ in range(n)]
    
    def reduce(self, x):
        for i in range(self.n - 1, -1, -1):
            if x >> i & 1:
                x ^= self.base[i]
        return x

    def add(self, x):
        x = self.reduce(x)
        if x:
            for i in range(self.n - 1, -1, -1):
                if (x >> i) & 1:
                    self.base[i] = x
                    return True
        return False
    
    def check(self, x):
        return self.reduce(x) == 0