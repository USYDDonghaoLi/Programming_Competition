class Trie:

    def __init__(self, n, mx) -> None:
        '''
        n: 数组长度
        mx: 最大值
        '''
        self.n = n
        self.mx = mx + 1
        self.k = self.mx.bit_length()
        self.LEN = self.n * self.k + 1

        self.zero_side = [-1 for _ in range(self.LEN)]
        self.one_side = [-1 for _ in range(self.LEN)]
        self.counts = [0 for _ in range(self.LEN)]
        self.nxt_node = 1
    
    def insert(self, num):
        node = 0
        for i in range(self.k - 1, -1, -1):
            self.counts[node] += 1
            if num >> i & 1:
                if self.one_side[node] == -1:
                    self.one_side[node] = self.nxt_node
                    self.nxt_node += 1
                node = self.one_side[node]
            else:
                if self.zero_side[node] == -1:
                    self.zero_side[node] = self.nxt_node
                    self.nxt_node += 1
                node = self.zero_side[node]
        self.counts[node] += 1
    
    def delete(self, num):
        node = 0
        for i in range(self.k - 1, -1, -1):
            self.counts[node] -= 1
            if num >> i & 1:
                node = self.one_side[node]
            else:
                node = self.zero_side[node]
    
    def findMaxXor(self, v):
        node = 0
        res = 0
        for i in range(self.k - 1, -1, -1):
            if v >> i & 1:
                if self.zero_side[node] and self.counts[self.zero_side[node]]:
                    node = self.zero_side[node]
                    res |= 1 << i
                else:
                    node = self.one_side[node]
            else:
                if self.one_side[node] and self.counts[self.one_side[node]]:
                    node = self.one_side[node]
                    res |= 1 << i
                else:
                    node = self.zero_side[node]
        return res

    def findMinXor(self, v):
        node = 0
        res = 0
        for i in range(self.k - 1, -1, -1):
            if v >> i & 1:
                if self.one_side[node] and self.counts[self.one_side[node]]:
                    node = self.one_side[node]
                else:
                    node = self.one_side[node]
                    res |= 1 << i
            else:
                if self.zero_side[node] and self.counts[self.zero_side[node]]:
                    node = self.zero_side[node]
                else:
                    node = self.zero_side[node]
                    res |= 1 << i
    
    def countXorLessThan(self, num, limit):
        node = 0
        count = 0
        for i in range(self.k - 1, -1, -1):
            bitVal = (num >> i) & 1
            limitBit = (limit >> i) & 1
            if limitBit:
                if self.zero_side[node] != -1:
                    count += self.counts[self.zero_side[node]]
                node = self.one_side[node] if bitVal == 0 else self.zero_side[node]
            else:
                node = self.zero_side[node] if bitVal == 0 else self.one_side[node]
            if node == -1:
                break
        return count

    def countXorLessThanEqual(self, num, limit):
        return self.countXorLessThan(num, limit + 1)

    def countXorGreaterThan(self, num, limit):
        total = self.counts[0]
        return total - self.countXorLessThanEqual(num, limit)

    def countXorGreaterThanEqual(self, num, limit):
        total = self.counts[0]
        return total - self.countXorLessThan(num, limit)
    