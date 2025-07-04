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

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

class Dijkstra:
    def __init__(self, n) -> None:
        self.n = n
        self.graph = defaultdict(list)
    
    
    def addedge(self, e1, e2, weight = 1):
        self.graph[e1].append((e2, weight))
        # self.graph[e2].append((e1, weight))
    
    def f(self, u, v):
        return u << 20 ^ v
    
    def sol(self, src):
        self.prev = [-1 for _ in range(self.n)]
        self.distance = [float('inf') for _ in range(self.n)]
        pq = []
        self.distance[src] = 0
        heappush(pq, self.f(0, src))
        
        while pq:
            z = heappop(pq)
            cost, cur = z >> 20, z & 0xfffff
            if cost > self.distance[cur]:
                continue
            for o, c in self.graph[cur]:
                if cost + c < self.distance[o]:
                    heappush(pq, self.f(cost + c, o))
                    self.distance[o] = cost + c
                    self.prev[o] = cur

    def check(self, start, end, flag = False):
        self.sol(start)
        routes = []
        if flag:
            routes = self.checkroute(end)
        return self.distance[end], routes
    
    def checkroute(self, end):
        cur = end
        routes = []
        while cur != -1:
            routes.append(cur)
            cur = self.prev[cur]
        return routes[::-1]

inf = float('inf')

class Tarjan:
    def __init__(self):
        return
 
    @staticmethod
    def get_scc(n: int, edge):
        assert all(i not in edge[i] for i in range(n))
        assert all(len(set(edge[i])) == len(edge[i]) for i in range(n))
        dfs_id = 0
        order, low = [inf] * n, [inf] * n
        visit = [0] * n
        out = []
        in_stack = [0] * n
        scc_id = 0
        # nodes list of every scc_id part
        scc_node_id = []
        # index if original node and value is scc_id part
        node_scc_id = [-1] * n
        parent = [-1] * n
        for node in range(n):
            if not visit[node]:
                stack = [[node, 0]]
                while stack:
                    cur, ind = stack[-1]
                    if not visit[cur]:
                        visit[cur] = 1
                        order[cur] = low[cur] = dfs_id
                        dfs_id += 1
                        out.append(cur)
                        in_stack[cur] = 1
                    if ind == len(edge[cur]):
                        stack.pop()
                        if order[cur] == low[cur]:
                            while out:
                                top = out.pop()
                                in_stack[top] = 0
                                while len(scc_node_id) < scc_id + 1:
                                    scc_node_id.append(set())
                                scc_node_id[scc_id].add(top)
                                node_scc_id[top] = scc_id
                                if top == cur:
                                    break
                            scc_id += 1
 
                        cur, nex = parent[cur], cur
                        if cur != -1:
                            low[cur] = low[cur] if low[cur] < low[nex] else low[nex]
                    else:
                        nex = edge[cur][ind]
                        stack[-1][-1] += 1
                        if not visit[nex]:
                            parent[nex] = cur
                            stack.append([nex, 0])
                        elif in_stack[nex]:
                            low[cur] = low[cur] if low[cur] < order[nex] else order[nex]
 
        # new graph after scc
        new_dct = [set() for _ in range(scc_id)]
        for i in range(n):
            for j in edge[i]:
                a, b = node_scc_id[i], node_scc_id[j]
                if a != b:
                    new_dct[a].add(b)
        new_degree = [0] * scc_id
        for i in range(scc_id):
            for j in new_dct[i]:
                new_degree[j] += 1
        assert len(scc_node_id) == scc_id
        return scc_id, scc_node_id, node_scc_id
 
    @staticmethod
    def get_pdcc(n: int, edge):
 
        dfs_id = 0
        order, low = [inf] * n, [inf] * n
        visit = [False] * n
        out = []
        parent = [-1] * n
        # number of group
        group_id = 0
        # nodes list of every group part
        group_node = []
        # index is original node and value is group_id set
        # cut node belong to two or more group
        node_group_id = [set() for _ in range(n)]
        child = [0] * n
        for node in range(n):
            if not visit[node]:
                stack = [[node, 0]]
                while stack:
                    cur, ind = stack[-1]
                    if not visit[cur]:
                        visit[cur] = True
                        order[cur] = low[cur] = dfs_id
                        dfs_id += 1
 
                    if ind == len(edge[cur]):
                        stack.pop()
                        cur, nex = parent[cur], cur
                        if cur != -1:
                            low[cur] = low[cur] if low[cur] < low[nex] else low[nex]
                            # cut node with rooted or not-rooted
                            if (parent == -1 and child[cur] > 1) or (parent != -1 and low[nex] >= order[cur]):
                                while out:
                                    top = out.pop()
                                    while len(group_node) < group_id + 1:
                                        group_node.append(set())
                                    group_node[group_id].add(top[0])
                                    group_node[group_id].add(top[1])
                                    node_group_id[top[0]].add(group_id)
                                    node_group_id[top[1]].add(group_id)
                                    if top == (cur, nex):
                                        break
                                group_id += 1
                            # We add all the edges encountered during deep search to the stack
                            # and when we find a cut point
                            # Pop up all the edges that this cutting point goes down to
                            # and the points connected by these edges are a pair of dots
                    else:
                        nex = edge[cur][ind]
                        stack[-1][-1] += 1
                        if nex == parent[cur]:
                            continue
                        if not visit[nex]:
                            parent[nex] = cur
                            out.append((cur, nex))
                            child[cur] += 1
                            stack.append([nex, 0])
                        elif low[cur] > order[nex]:
                            low[cur] = order[nex]
                            out.append((cur, nex))
            if out:
                while out:
                    top = out.pop()
                    group_node[group_id].add(top[0])
                    group_node[group_id].add(top[1])
                    node_group_id[top[0]].add(group_id)
                    node_group_id[top[1]].add(group_id)
                group_id += 1
        return group_id, group_node, node_group_id
 
    def get_edcc(self, n: int, edge):
        _, cutting_edges = self.get_cut(n, [list(e) for e in edge])
        for i, j in cutting_edges:
            edge[i].discard(j)
            edge[j].discard(i)
        # Remove all cut edges and leaving only edge doubly connected components
        # process the cut edges and then perform bfs on the entire undirected graph
        visit = [0] * n
        edcc_node_id = []
        for i in range(n):
            if visit[i]:
                continue
            stack = [i]
            visit[i] = 1
            cur = [i]
            while stack:
                x = stack.pop()
                for j in edge[x]:
                    if not visit[j]:
                        visit[j] = 1
                        stack.append(j)
                        cur.append(j)
            edcc_node_id.append(cur[:])
 
        # new graph after edcc
        edcc_id = len(edcc_node_id)
        node_edcc_id = [-1] * n
        for i, ls in enumerate(edcc_node_id):
            for x in ls:
                node_edcc_id[x] = i
        new_dct = [[] for _ in range(edcc_id)]
        for i in range(n):
            for j in edge[i]:
                a, b = node_edcc_id[i], node_edcc_id[j]
                if a != b:
                    new_dct[a].append(b)
        new_degree = [0] * edcc_id
        for i in range(edcc_id):
            for j in new_dct[i]:
                new_degree[j] += 1
        return edcc_node_id
 
    @staticmethod
    def get_cut(n: int, edge):
        order, low = [inf] * n, [inf] * n
        visit = [0] * n
        cutting_point = set()
        cutting_edge = []
        child = [0] * n
        parent = [-1] * n
        dfs_id = 0
        for i in range(n):
            if not visit[i]:
                stack = [[i, 0]]
                while stack:
                    cur, ind = stack[-1]
                    if not visit[cur]:
                        visit[cur] = 1
                        order[cur] = low[cur] = dfs_id
                        dfs_id += 1
                    if ind == len(edge[cur]):
                        stack.pop()
                        cur, nex = parent[cur], cur
                        if cur != -1:
                            pa = parent[cur]
                            low[cur] = low[cur] if low[cur] < low[nex] else low[nex]
                            if low[nex] > order[cur]:
                                cutting_edge.append((cur, nex) if cur < nex else (nex, cur))
                            if pa != -1 and low[nex] >= order[cur]:
                                cutting_point.add(cur)
                            elif pa == -1 and child[cur] > 1:
                                cutting_point.add(cur)
                    else:
                        nex = edge[cur][ind]
                        stack[-1][-1] += 1
                        if nex == parent[cur]:
                            continue
                        if not visit[nex]:
                            parent[nex] = cur
                            child[cur] += 1
                            stack.append([nex, 0])
                        else:
                            low[cur] = low[cur] if low[cur] < order[nex] else order[nex]
        return cutting_point, cutting_edge

# @TIME
def solve(testcase):
    n, m = MI()

    edges = []
    D1 = Dijkstra(n)
    D2 = Dijkstra(n)
    mp = defaultdict(int)

    for i in range(m):
        a, b, c = MI()
        a -= 1
        b -= 1
        edges.append((a, b, c))
        D1.addedge(a, b, c)
        D1.addedge(b, a, c)
        D2.addedge(a, b, c)
        D2.addedge(b, a, c)
        mp[(a, b)] = i
        mp[(b, a)] = i
    
    D1.sol(0)

    D2.sol(n - 1)

    min_dist = D1.distance[n - 1]

    # print(D1.distance)

    newG = defaultdict(list)

    for a, b, c in edges:
        if abs(D1.distance[b] - D1.distance[a]) == c and abs(D2.distance[b] - D2.distance[a]) == c and fmin(D1.distance[a] + D2.distance[b], D1.distance[b] + D2.distance[a]) + c == min_dist:
            newG[a].append(b)
            newG[b].append(a)
    
    # print(newG)

    _, cutting_edge = Tarjan().get_cut(n, newG)

    # print(cutting_edge)

    res = ['No' for _ in range(m)]

    for u, v in cutting_edge:
        assert (u, v) in mp
        res[mp[(u, v)]] = 'Yes'
    
    print('\n'.join(res))

for testcase in range(1):
    solve(testcase)