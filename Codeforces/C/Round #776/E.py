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

#------------------------------FastIO---------------------------------



def solve():

    def ops(arr):
        #print('arr', arr)
        m = len(arr)
        mx, mi = float('-inf'), float('inf')
        for i in range(m - 1):
            temp = arr[i + 1] - arr[i] - 1
            mx = max(mx, temp)
            mi = min(mi, temp)
    
        return min(mi, max((mx - 1) >> 1, d - arr[-1] - 1))
    
    input()
    n, d = MI()
    nums = [0] + LII()
    n = len(nums)

    helper = []
    for i in range(n - 1):
        helper.append(nums[i + 1] - nums[i] - 1)
    
    idx = -1
    res = float('inf')

    for i in range(len(helper)):
        if res > helper[i]:
            idx = i
            res = helper[i]
        
    if idx:
        temp = nums[:idx] + nums[idx + 1:]
        res = max(res, ops(temp))
    
    temp = nums[:idx + 1] + nums[idx + 2:]
    res = max(res, ops(temp))
    print(res)
    
for _ in range(int(input())):solve()