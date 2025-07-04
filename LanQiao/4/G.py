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

# from types import GeneratorType
# def bootstrap(f, stack=[]):
#     def wrappedfunc(*args, **kwargs):
#         if stack:
#             return f(*args, **kwargs)
#         else:
#             to = f(*args, **kwargs)
#             while True:
#                 if type(to) is GeneratorType:
#                     stack.append(to)
#                     to = next(to)
#                 else:
#                     stack.pop()
#                     if not stack:
#                         break
#                     to = stack[-1].send(to)
#             return to
#     return wrappedfunc

# seed(19981220)
# RANDOM = getrandbits(64)
 
# class Wrapper(int):
#     def __init__(self, x):
#         int.__init__(x)

#     def __hash__(self):
#         return super(Wrapper, self).__hash__() ^ RANDOM

# def TIME(f):

#     def wrap(*args, **kwargs):
#         s = perf_counter()
#         ret = f(*args, **kwargs)
#         e = perf_counter()

#         print(e - s, 'sec')
#         return ret
    
#     return wrap

inf = float('inf')

class mcf_graph:
    n = 1
    pos = []
    g = [[]]

    def __init__(self, N):
        self.n = N
        self.pos = []
        self.g = [[] for _ in range(N)]

    def add_edge(self, From, To, cap, cost):
        assert 0 <= From and From < self.n
        assert 0 <= To and To < self.n
        m = len(self.pos)
        # print(From, To, cap, cost)
        self.pos.append((From ,len(self.g[From])))
        self.g[From].append({"to": To, "rev": len(self.g[To]), "cap": cap, "cost": cost})
        self.g[To].append({"to": From,"rev": len(self.g[From]) - 1,"cap": 0, "cost": -cost})

    def get_edge(self,i):
        m = len(self.pos)
        assert 0 <= i and i < m
        _e = self.g[self.pos[i][0]][self.pos[i][1]]
        _re = self.g[_e["to"]][_e["rev"]]
        return {"from": self.pos[i][0], "to": _e["to"], "cap": _e["cap"] + _re["cap"], "flow" : _re["cap"], "cost" : _e["cost"]}

    def edges(self):
        m = len(self.pos)
        result=[{} for _ in range(m)]
        for i in range(m):
            tmp = self.get_edge(i)
            result[i]["from"] = tmp["from"]
            result[i]["to"] = tmp["to"]
            result[i]["cap"] = tmp["cap"]
            result[i]["flow"] = tmp["flow"]
            result[i]["cost"] = tmp["cost"]
        return result

    #here we get the result
    def flow(self, s, t, flow_limit = (1 << 63) - 1):
        return self.slope(s,t,flow_limit)[-1]

    def slope(self, s, t, flow_limit = (1 << 63) - 1):
        assert 0 <= s and s < self.n
        assert 0 <= t and t < self.n
        assert s != t
        '''
         variants (C = maxcost):
         -(n-1)C <= dual[s] <= dual[i] <= dual[t] = 0
         reduced cost (= e.cost + dual[e.from] - dual[e.to]) >= 0 for all edge
        '''
        dual = [0 for _ in range(self.n)]
        dist = [0 for __ in range(self.n)]
        pv = [0 for _ in range(self.n)]
        pe = [0 for _ in range(self.n)]
        vis = [False for _ in range(self.n)]
        def dual_ref():
            for i in range(self.n):
                dist[i] = (1 << 63) - 1
                pv[i] = -1
                pe[i] = -1
                vis[i] = False
            que = []
            heappush(que, (0 ,s))
            dist[s] = 0
            while(que):
                v = heappop(que)[1]
                if vis[v]:
                    continue
                vis[v] = True
                if v == t:
                    break
                '''
                 dist[v] = shortest(s, v) + dual[s] - dual[v]
                 dist[v] >= 0 (all reduced cost are positive)
                 dist[v] <= (n-1)C
                '''
                for i in range(len(self.g[v])):
                    e = self.g[v][i]
                    if vis[e["to"]] or (not(e["cap"])):
                        continue
                    '''
                     |-dual[e.to]+dual[v]| <= (n-1)C
                     cost <= C - -(n-1)C + 0 = nC
                    '''
                    cost = e["cost"] - dual[e["to"]] + dual[v]
                    if dist[e["to"]] - dist[v] > cost:
                        dist[e["to"]] = dist[v] + cost
                        pv[e["to"]] = v
                        pe[e["to"]] = i
                        heappush(que, (dist[e["to"]] ,e["to"]))
            if not(vis[t]):
                return False
            for v in range(self.n):
                if not (vis[v]):
                    continue
                dual[v] -= dist[t] - dist[v]
            return True

        flow = 0
        cost = 0
        prev_cost = -1
        result=[(flow, cost)]
        while  flow < flow_limit:
            if not (dual_ref()):
                break
            c = flow_limit - flow
            v = t
            while(v != s):
                c = min(c, self.g[pv[v]][pe[v]]["cap"])
                v = pv[v]
            v = t
            while(v != s):
                self.g[pv[v]][pe[v]]["cap"] -= c
                self.g[v][self.g[pv[v]][pe[v]]["rev"]]["cap"] += c
                v = pv[v]
            d = -dual[s]
            flow += c
            cost += c*d
            if(prev_cost == d):
                result.pop()
            result.append((flow, cost))
            prev_cost = cost
        return result

# @TIME
def solve(testcase):
    n = II()
    A = LII()
    pre = [0 for _ in range(11)]
    pre11 = defaultdict(int)
    
    mcmf = mcf_graph(2 * n + 10)
    S, T = 2 * n + 1, 2 * n + 2
    
    for i, v in enumerate(A, 1):
        mcmf.add_edge(S, i, 1, 0)
        mcmf.add_edge(i + n, T, 1, 0)
        mcmf.add_edge(i, i + n, 1, -1)
        
        if pre[v % 9]:
            mcmf.add_edge(pre[v % 9], i, 10000, 0)
            mcmf.add_edge(pre[v % 9] + n, i, 10000, 0)
        
        if v - 11 in pre11:
            mcmf.add_edge(pre11[v - 11], i, 10000, 0)
            mcmf.add_edge(pre11[v - 11] + n, i, 10000, 0)
        
        if v + 11 in pre11:
            mcmf.add_edge(pre11[v + 11], 1, 10000, 0)
            mcmf.add_edge(pre11[v + 11] + n, i, 10000, 0)
        
        pre[v % 9] = i
        pre11[v] = i
    
    mcmf.add_edge(n + 1, T, 1, 0)

    # print(mcmf.g)
    
    res = []
    for a, b in mcmf.slope(S, T)[1:]:
        res.append(-b)
    
    while len(res) < n:
        res.append(res[-1])
    
    print(*res)

for testcase in range(1):
    solve(testcase)