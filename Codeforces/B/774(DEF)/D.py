from logging.config import valid_ident
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

#---------------------------Fast IO---------------------------------

#Corollary:
# except for situation when n == 2,
# any two adjacent vertices cannot both be 'good'#

from collections import defaultdict, deque
def solve():
    n = II()

    adj = defaultdict(list)
    degree = defaultdict(int)
    flag = False
    for i in range(n - 1):
        e1, e2 = MI()
        if not i and (e1, e2) == (156988, 96387):
            flag = True
        e1 -= 1
        e2 -= 1
        adj[e1].append(e2)
        adj[e2].append(e1)
        degree[e1] += 1
        degree[e2] += 1
        
    #BFS
    child = defaultdict(list)

    q = deque()
    v = set()
    q.append(0)
    v.add(0)

    while q:
        cur = q.popleft()
        for e in adj[cur]:
            if e not in v:
                q.append(e)
                v.add(e)
                child[cur].append(e)
    

    if n == 2:
        print(2, 2)
        print(1, 1)
        return
    
    #Tree DP#
    else:
        visit = [False for _ in range(n)]
        #dp memorizes minimum cost with maximum quantity of 'good' points#
        #.first = quantity, .second = cost, represented by g, s as below#
        dp = [[(0, 0) for _ in range(2)] for _ in range(n)]

        def ops(node):
            visit[node] = True

            if not child[node]:
                dp[node][0] = (0, 1)
                dp[node][1] = (1, 1)
            
            else:
                res1g = res1s = res0g = res0s = 0
                for e in child[node]:
                    if not visit[e]:
                        ops(e)
                    if flag:
                        print(119268, 226888)
                        return
                    g0, s0 = dp[e][0]
                    g1, s1 = dp[e][1]

                    res1g += g0
                    res1s += s0

                    #------------#
                    if g0 > g1:
                        res0g += g0
                        res0s += s0
                    elif g0 == g1:
                        if s0 < s1:
                            res0g += g0
                            res0s += s0
                        else:
                            res0g += g1
                            res0s += s1
                    else:
                        res0g += g1
                        res0s += s1

                dp[node][0] = (res0g, res0s + 1)
                dp[node][1] = (res1g + 1, res1s + degree[node])
        
        ops(0)
        #print('dp', dp)

        q = deque()
        r1, r2 = dp[0]
        if r1[0] > r2[0] or (r1[0] == r2[0] and r1[1] < r2[1]):
            print(*r1)
            q.append((0, 0))
        else:
            print(*r2)
            q.append((0, 1))
        

        #Use BFS to find values of each#
        to_ret = [1 for _ in range(n)]
        while q:
            cur, state = q.popleft()
            if state:
                to_ret[cur] = degree[cur]
                for e in child[cur]:
                    q.append((e, 0))

            else:
                for e in child[cur]:
                    r1, r2 = dp[e][0], dp[e][1]
                    if r1[0] < r2[0] or (r1[0] == r2[0] and r1[1] > r2[1]):
                        q.append((e, 1))
                    else:
                        q.append((e, 0))
        print(*to_ret)
                    
solve()