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
from random import *
#dfs - stack#



def solve():
    n = randint(1, 2000)
    arr = [i for i in range(1, n + 1)]
    shuffle(arr)
    lst = [(i + 1) // arr[i] for i in range(n)]

    #n = II()
    v = [False for _ in range(n + 1)]
    res = [-1 for _ in range(n + 1)]
    #lst = LII()
    def func(val, idx):
        if val == 0:
            return n - idx 
        else:
            return idx // val - idx // (val + 1)
    nums = sorted([(v, i + 1) for i, v in enumerate(lst)], key = lambda x: func(x[0], x[1]))
    #print('nums', nums)
    
    while True:
        for val, idx in nums:
            flag = False
            if val == 0:
                for _ in range(1000):
                    num = randint(idx + 1, n)
                    if v[num]:
                        continue
                    else:
                        v[num] = True
                        res[idx] = num
                        flag = True
                        break
            else:
                for _ in range(1000):
                    num = randint(idx // (val + 1) + 1, idx // val)
                    if v[num]:
                        continue
                    else:
                        v[num] = True
                        res[idx] = num
                        flag = True
                        break
        if not flag:
            res = [-1 for _ in range(n)]
            continue
        else:
            break
        
    print(*res[1:])
    if all(i // res[i] == i // arr[i - 1] for i in range(1, n + 1)):
        print('AC')
    else:
        print('WA')
        print(res.count(-1))
        exit()
        # print(res)
        # print('lst', lst)
        # print('arr', arr)
        # exit()
for _ in range(II()):solve()