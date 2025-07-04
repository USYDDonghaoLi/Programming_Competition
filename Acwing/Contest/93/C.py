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

RANDOM = getrandbits(32)
 
class Wrapper(int):
    def __init__(self, x):
        int.__init__(x)
 
    def __hash__(self):
        return super(Wrapper, self).__hash__() ^ RANDOM

class Trie:

    def __init__(self):
        self.left = None
        self.right = None
        self.cnt = 0
    
    def insert(self, num):
        cur = self
        cur.cnt += 1
        for i in range(30, -1, -1):
            ID = num >> i & 1
            if ID:
                if cur.right == None:
                    cur.right = Trie()
                cur = cur.right
            else:
                if cur.left == None:
                    cur.left = Trie()
                cur = cur.left
            cur.cnt += 1
    
    def sol(self, tot):
        res = 0
        cur = self
        for i in range(30, -1, -1):
            if cur.left.cnt == tot:
                cur = cur.left
            else:
                res |= 1 << i
                cur = cur.right
                tot = cur.cnt
            print(i, res)
        return res

    def delete(self, num):
        cur = self
        cur.cnt -= 1
        for i in range(30, -1, -1):
            ID = num >> i & 1
            if ID:
                if cur.right == None:
                    cur.right = Trie()
                cur = cur.right
            else:
                if cur.left == None:
                    cur.left = Trie()
                cur = cur.left
            cur.cnt -= 1
    
    def query_max(self, num):
        cur = self
        res = 0
        for i in range(30, -1, -1):
            ID = num >> i & 1
            if ID:
                '''
                带删除的版本
                '''
                # if cur.left != None and cur.left.cnt:
                #     res |= 1 << i
                #     cur = cur.left
                # elif cur.right != None and cur.right.cnt:
                #     cur = cur.right
                # else:
                #     break

                if cur.left != None:
                    res |= 1 << i
                    cur = cur.left
                elif cur.right != None:
                    cur = cur.right
                else:
                    break
            else:
                '''
                带删除的版本
                '''
                # if cur.right != None and cur.right.cnt:
                #     res |= 1 << i
                #     cur = cur.right
                # elif cur.left != None and cur.left.cnt:
                #     cur = cur.left
                # else:
                #     break

                if cur.right != None:
                    res |= 1 << i
                    cur = cur.right
                elif cur.left != None:
                    cur = cur.left
                else:
                    break
        return res

    '''
    与数组中xor后小于limit的元素个数
    '''
    def query_less_than_limit(self, num, limit):
        res = 0
        cur = self
        for i in range(30, -1, -1):
            ID = num >> i & 1
            L = limit >> i & 1
            try:
                if ID:
                    if L:
                        try:
                            res += cur.right.cnt
                        except:
                            pass
                        cur = cur.left
                    else:
                        cur = cur.right
                else:
                    if L:
                        try:
                            res += cur.left.cnt
                        except:
                            pass
                        cur = cur.right
                    else:
                        cur = cur.left
            except:
                break
        return res


def solve(testcase):
    n = II()
    nums = LII()

    # bits = [0 for _ in range(30)]
    def calc(nums, bit):
        if bit == -1:
            return 0
        if not nums:
            return float('inf')
        zero = []
        one = []
        # print('nums', nums)
        for num in nums:
            if num >> bit & 1:
                one.append(num)
            else:
                zero.append(num)
        # print(one, zero)
        if len(zero) == 0 or len(zero) == len(nums):
            return calc(nums, bit - 1)
        else:
            return min(max(calc(zero, bit - 1), calc(one, bit - 1) | (1 << bit)), max(calc(one, bit - 1), calc(zero, bit - 1) | (1 << bit)))

    print(calc(nums, 30))


for testcase in range(1):
    solve(testcase)