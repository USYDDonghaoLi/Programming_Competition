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

from heapq import heappush, heappop
def solve():
    n = int(input())
    helper = []
    temp = 0
    for _ in range(n << 1):
        info = input().split()
        if info[0] == '+':
            temp += 1
        else:
            temp -= 1
        helper.append(info)
    
    pq = []
    to_ret = []

    flag = False
    for i in range(2 * n - 1, -1, -1):
        temp = helper[i]
        if len(temp) == 2:
            if flag and int(helper[i + 1][1]) < int(temp[1]):
                print('NO')
                return
            else:
                heappush(pq, int(temp[1]))

            if i - 1 >= 0 and len(helper[i - 1]) == 2:
                flag = True
            else:
                flag = False
        
        else:
            if not pq:
                print('NO')
                return
            
            else:
                to_ret.append(heappop(pq))
            
            flag = False
        
    temp = to_ret.copy()
    pq = []
    for order in helper:
        if order[0] == '+':
            heappush(pq, temp.pop())
        else:
            cur = heappop(pq)
            if cur != int(order[1]):
                print('NO')
                return
    
    
    print('YES')
    print(*to_ret[::-1])
    return

solve()        

