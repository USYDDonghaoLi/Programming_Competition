'''
Hala Madrid!
https://www.zhihu.com/people/li-dong-hao-78-74
'''

import sys
import os
from io import BytesIO, IOBase
BUFSIZE = 8192
class FastIO(IOBase):
    newlines = 0
    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None
    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()
    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()
    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)
class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")
sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

def I():
    return input()
def II():
    return int(input())
def MI():
    return map(int, input().split())
def LI():
    return list(input().split())
def LII():
    return list(map(int, input().split()))
def GMI():
    return map(lambda x: int(x) - 1, input().split())

#------------------------------FastIO---------------------------------

from bisect import *
from heapq import *
from collections import *
from functools import *
from itertools import *
from time import *
from random import *
from math import log, gcd, sqrt, ceil

'''
手写栈防止recursion limit
注意要用yield 不要用return
函数结尾要写yield None
'''
from types import GeneratorType
def bootstrap(f, stack=[]):
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to
    return wrappedfunc
    
class Trie:
    N = 30
    def __init__(self):
        self.left = None
        self.right = None
        self.cnt = 0
    
    def insert(self, x: int) -> None:
        root = self
        self.cnt += 1
        for i in range(Trie.N, -1, -1):
            ID = (x >> i) & 1
            if ID == 0:
                if root.left == None:
                    root.left = Trie()
                root = root.left
            else:
                if root.right == None:
                    root.right = Trie()
                root = root.right
            root.cnt += 1
    
    def delete(self, x: int) -> None:
        root = self
        self.cnt -= 1
        for i in range(Trie.N, -1, -1):
            ID = (x >> i) & 1
            if ID == 0:
                if root.left == None:
                    root.left = Trie()
                root = root.left
            else:
                if root.right == None:
                    root.right = Trie()
                root = root.right
            root.cnt -= 1
    
    def query_min(self, x: int) -> int:
        root = self
        res = 0
        for i in range(Trie.N, -1, -1):
            ID = (x >> i) & 1
            if ID == 0:
                if root.left != None:
                    root = root.left
                elif root.right != None:
                    res |= 1 << i
                    root = root.right
                else:
                    break
            else:
                if root.right != None:
                    root = root.right
                elif root.left != None:
                    res |= 1 << i
                    root = root.left
                else:
                    break
        return res
    
    def query_max(self, x: int) -> int:
        root = self
        res = 0
        for i in range(Trie.N, -1, -1):
            ID = (x >> i) & 1
            if ID == 0:
                if root.right != None and root.right.cnt:
                    res |= 1 << i
                    root = root.right
                elif root.left != None:
                    root = root.left
                else:
                    break
            else:
                if root.left != None and root.left.cnt:
                    res |= 1 << i
                    root = root.left
                elif root.right != None:
                    root = root.right
                else:
                    break
        return res

mod = 10 ** 9 + 7

@lru_cache(None)
def inv(num):
    return pow(num, mod - 2, mod)

def solve(testcase):
    n = II()
    A = LII()
    TRIE = Trie()
    adj = defaultdict(list)
    for _ in range(n - 1):
        u, v = MI()
        adj[u].append(v)
        adj[v].append(u)
    
    value = [-1 for _ in range(n + 1)]
    value[1] = A[0]
    child = defaultdict(list)
    @bootstrap
    def dfs(node, parent):
        for o in adj[node]:
            if o == parent:
                continue
            else:
                child[node].append(o)
                value[o] = value[node] ^ A[o - 1]
                yield dfs(o, node)
        yield None
    
    dfs(1, 0)

    prob = [-1 for _ in range(n + 1)]
    prob[1] = 1
    res = 0

    @bootstrap
    def dfs2(node):
        nonlocal res
        TRIE.insert(A[node - 1])
        if child[node]:
            p = prob[node] * inv(len(child[node])) % mod
            for o in child[node]:
                prob[o] = p
                yield dfs2(o)
        else:
            res += prob[node] * TRIE.query_max(value[node]) % mod
            res %= mod
        
        TRIE.delete(A[node - 1])
        yield None
    
    dfs2(1)

    print(res)


for testcase in range(II()):
    solve(testcase)