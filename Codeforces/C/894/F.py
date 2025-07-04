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

# '''
# 手写栈防止recursion limit
# 注意要用yield 不要用return
# 函数结尾要写yield None
# '''
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

# RANDOM = getrandbits(32)
 
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

from collections import deque
class mf_graph:
    n=1
    g=[[] for i in range(1)]
    pos=[]
    def __init__(self,N):
        self.n=N
        self.g=[[] for i in range(N)]
        self.pos=[]
    def add_edge(self,From,To,cap):
        assert 0<=From and From<self.n
        assert 0<=To and To<self.n
        assert 0<=cap
        m=len(self.pos)
        self.pos.append((From,len(self.g[From])))
        self.g[From].append({"to":To,"rev":len(self.g[To]),"cap":cap})
        self.g[To].append({"to":From,"rev":len(self.g[From])-1,"cap":0})
        return m
    def get_edge(self,i):
        m=len(self.pos)
        assert 0<=i and i<m
        _e=self.g[self.pos[i][0]][self.pos[i][1]]
        _re=self.g[_e["to"]][_e["rev"]]
        return {"from":self.pos[i][0],
                "to":_e["to"],
                "cap":_e["cap"]+_re["cap"],
                "flow":_re["cap"]}
    def edges(self):
        m=len(self.pos)
        result=[]
        for i in range(m):
            result.append(self.get_edge(i))
        return result
    def change_edge(self,i,new_cap,new_flow):
        m=len(self.pos)
        assert 0<=i and i<m
        assert 0<=new_flow and new_flow<=new_cap
        _e=self.g[self.pos[i][0]][self.pos[i][1]]
        _re=self.g[_e["to"]][_e["rev"]]
        _e["cap"]=new_cap-new_flow
        _re["cap"]=new_flow
    def flow(self,s,t,flow_limit=(1<<63)-1):
        assert 0<=s and s<self.n
        assert 0<=t and t<self.n
        level=[0 for i in range(self.n)]
        Iter=[0 for i in range(self.n)]
        que=deque([])
        def bfs():
            for i in range(self.n):level[i]=-1
            level[s]=0
            que=deque([])
            que.append(s)
            while(len(que)>0):
                v=que.popleft()
                for e in self.g[v]:
                    if e["cap"]==0 or level[e["to"]]>=0:continue
                    level[e["to"]]=level[v]+1
                    if e["to"]==t:return
                    que.append(e["to"])
        def dfs(func,v,up):
            if (v==s):return up
            res=0
            level_v=level[v]
            for i in range(Iter[v],len(self.g[v])):
                e=self.g[v][i]
                if (level_v<=level[e["to"]] or self.g[e["to"]][e["rev"]]["cap"]==0):continue
                d=func(func,e["to"],min(up-res,self.g[e["to"]][e["rev"]]["cap"]))
                if d<=0:continue
                self.g[v][i]["cap"]+=d
                self.g[e["to"]][e["rev"]]["cap"]-=d
                res+=d
                if res==up:return res
            level[v]=self.n
            return res
        flow=0
        while(flow<flow_limit):
            bfs()
            if level[t]==-1:break
            for i in range(self.n):Iter[i]=0
            while(flow<flow_limit):
                f=dfs(dfs,t,flow_limit-flow)
                if not(f):break
                flow+=f
        return flow
    def min_cut(self,s):
        visited=[False for i in range(self.n)]
        que=deque([])
        que.append(s)
        while(len(que)>0):
            p=que.popleft()
            visited[p]=True
            for e in self.g[p]:
                if e["cap"] and not(visited[e["to"]]):
                    visited[e["to"]]=True
                    que.append(e["to"])
        return visited

# @TIME
def solve(testcase):
    w, f = MI()
    n = II()
    nums = LII()
    # s = sum(nums)
    nums.sort(reverse = True)

    '''
    SOURCE: n
    WATER: n + 1
    FIRE: n + 2
    END: n + 3
    '''

    def check(mid):
        water, fire = mid * w, mid * f
        for m in nums:
            if water >= fire:
                water -= m
            else:
                fire -= m
            if water < 0 or fire < 0:
                return False
        return True

    l, r = 1, 1000010
    while l < r:
        mid = l + r >> 1
        if check(mid):
            r = mid
        else:
            l = mid + 1
    
    print(l)


for testcase in range(II()):
    solve(testcase)