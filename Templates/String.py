class StringHash:

    __slots__ = {'n', 'base', 'mod', 'pw', 'hash_values'}

    def __init__(self, string, base = 131, mod = 10 ** 9 + 7) -> None:
        self.n = len(string)
        self.base = base
        self.mod = mod

        self.pw = [1 for _ in range(self.n + 10)]
        for i in range(1, self.n + 10):
            self.pw[i] = self.pw[i - 1] * self.base % self.mod

        self.hash_values = [0 for _ in range(self.n + 1)]
        for i in range(1, self.n + 1):
            self.hash_values[i] = (self.hash_values[i - 1] * self.base + ord(string[i - 1]) - ord('a') + 1) % self.mod
    

    def get_hash_val(self, left, right):
        assert right >= left
        return (self.hash_values[right + 1] - self.hash_values[left]) % self.mod
    
    def is_equal(self, left1, right1, left2, right2):
        assert right1 - left1 == right2 - left2
        return self.get_hash_val(left1, right1) * self.pw[left2 - left1] % self.mod == self.get_hash_val(left2, right2)

class Trie_Array:
    '''
    数组实现Trie
    '''
    __slots__ = {'n', 'nxt', 'cnt', 'exist'}

    def __init__(self, n) -> None:
        self.n = n
        self.nxt = [[0 for _ in range(26)] for _ in range(self.n)]
        self.cnt = 0
        self.exist = [False for _ in range(n)]
    
    def insert(self, s):
        p = 0 
        for ch in s:
            c = ord(ch) - ord('a')
            if not self.nxt[p][c]:
                self.cnt += 1
                self.nxt[p][c] = self.cnt
            p = self.nxt[p][c]
        self.exist[p] = True
    
    def find(self, s):
        p = 0
        for ch in s:
            c = ord(ch) - ord('a')
            if not self.nxt[p][c]:
                return False
            p = self.nxt[p][c]
        return self.exist[p]

class Trie:
    '''
    Node实现Trie
    '''
    def __init__(self) -> None:
        self.nxt = [None for _ in range(26)]
        self.isend = False
    
    def insert(self, s):
        cur = self
        for ch in s:
            c = ord(ch) - ord('a')
            if not cur.nxt[c]:
                cur.nxt[c] = Trie()
            cur = cur.nxt[c]
        cur.isend = True
    
    def find(self, s):
        cur = self
        for ch in s:
            c = ord(ch) - ord('a')
            if not cur.nxt[c]:
                return False
            cur = cur.nxt[c]
        return cur.isend
    
    def isprefix(self, s):
        cur = self
        for ch in s:
            c = ord(ch) - ord('a')
            if not cur.nxt[c]:
                return False
            cur = cur.nxt[c]
        return True

class Binary_Trie_Node:
    __slots__ = {'nxt'}

    def __init__(self) -> None:
        self.nxt = [None for _ in range(2)]
    
    def insert(self, n):
        cur = self
        for bit in range(31, -1, -1):
            t = n >> bit & 1
            if not cur.nxt[t]:
                cur.nxt[t] = Binary_Trie_Node()
            cur = cur.nxt[t]

    def findmax(self, n):
        res = 0
        cur = self
        for bit in range(31, -1, -1):
            t = n >> bit & 1
            if cur.nxt[t ^ 1]:
                res |= 1 << bit
                cur = cur.nxt[t ^ 1]
            else:
                cur = cur.nxt[t]
        return res
    
    def findmin(self, n):
        res = 0
        cur = self
        for bit in range(31, -1, -1):
            t = n >> bit & 1
            if self.nxt[t]:
                cur = cur.nxt[t]
            else:
                res |= 1 << bit
                cur = cur.nxt[t ^ 1]
        return res

class Binary_Trie:
    '''
    数组实现Trie
    '''
    __slots__ = {'n', 'nxt', 'cnt', 'exist'}

    def __init__(self, n) -> None:
        self.n = n
        self.nxt = [[0 for _ in range(2)] for _ in range(self.n)]
        self.cnt = 0
        #self.exist = [False for _ in range(n)]
    
    def insert(self, n):
        p = 0
        for bit in range(31, -1, -1):
            t = n >> bit & 1
            if not self.nxt[p][t]:
                self.cnt += 1
                self.nxt[p][t] = self.cnt
            p = self.nxt[p][t]
    
    def findmax(self, n):
        p = 0
        res = 0
        for bit in range(31, -1, -1):
            t = n >> bit & 1
            if self.nxt[p][t ^ 1]:
                res |= 1 << bit
                p = self.nxt[p][t ^ 1]
            else:
                p = self.nxt[p][t]
        return res
    
    def findmin(self, n):
        p = 0
        res = 0
        for bit in range(31, -1, -1):
            t = n >> bit & 1
            if self.nxt[p][t]:
                p = self.nxt[p][t]
            else:
                res |= 1 << bit
                p = self.nxt[p][t]
        return res

class Trie_xorsum:
    def __init__(self) -> None:
        self.MAXH = 31
        self.ch = [[0 for _ in range(2)] for _ in range(self.MAXH + 1)]
        self.w = [0 for _ in range(self.MAXH + 1)]
        self.xorv = [0 for _ in range(self.MAXH + 1)]
        self.tot = 0
    
    def mknode(self):
        self.tot += 1
        self.ch[self.tot][1] = self.ch[self.tot][0] = self.w[self.tot] = self.xorv[self.tot] = 0
        return self.tot
    
    def maintain(self, o):
        self.w[o] = self.xorv[o] = 0
        if self.ch[o][0]:
            self.w[o] += self.w[self.ch[o][0]]
            self.xorv[o] ^= self.xorv[self.ch[o][0]] << 1
        if self.ch[o][1]:
            self.w[o] += self.w[self.ch[o][1]]
            self.xorv[o] ^= (self.xorv[self.ch[o][1]] << 1) | (self.w[self.ch[o][1]] & 1)
        self.w[o] &= 1

    def insert(self, o, x, dp):
        if not o:
            o = self.mknode()
        if dp > self.MAXH:
            self.w[o] += 1
            return
        self.insert(self.ch[o][x & 1], x >> 1, dp + 1)
        self.maintain(o)
    
    def erase(self, o, x, dp):
        if dp > 30:
            self.w[o] -= 1
            return
        self.erase(self.ch[o][x & 1], x >> 1, dp + 1)
        self.maintain(o)
    
    def addall(self, o):
        self.ch[o][0], self.ch[o][1] = self.ch[o][1], self.ch[o][0]
        if self.ch[o][0]:
            self.addall(self.ch[o][0])
        self.maintain(o)
