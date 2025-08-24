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

import math

eps = 1e-9

import math

# Define epsilon for floating-point comparisons
eps = 1e-9

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return abs(self.x - other.x) <= eps and abs(self.y - other.y) <= eps

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __mul__(self, k):
        if isinstance(k, Point):
            '''
            点积
            '''
            return self.x * k.x + self.y * k.y
        return Point(k * self.x, k * self.y)

    def __truediv__(self, k):
        return Point(self.x / k, self.y / k)

    def __xor__(self, other):
        '''
        叉积
        '''
        return self.x * other.y - self.y * other.x

    def toleft(self, other):
        '''
        当前点相对于other的位置，正值表示在左，负值表示在右
        '''
        t = self ^ other
        return (t > eps) - (t < -eps)

    def len2(self):
        '''
        距离原点的平方距离
        '''
        return self * self

    def len(self):
        '''
        距离远点的距离
        '''
        return math.sqrt(self.len2())

    def dis2(self, other):
        '''
        当前节点相对于other的平方距离
        '''
        return (other - self).len2()

    def dis(self, other):
        '''
        当前节点相对于other的距离
        '''
        return math.sqrt(self.dis2(other))

    def rotate(self, alpha):
        return Point(
            self.x * math.cos(alpha) - self.y * math.sin(alpha),
            self.x * math.sin(alpha) + self.y * math.cos(alpha),
        )

class Line:
    def __init__(self, p: Point, v: Point):
        '''
        线由一个点 p 和一个向量 v 组成
        '''
        self.p = p
        self.v = v

    def toleft(self, a):
        '''
        a 相对于线的方向
        '''
        return self.v.toleft(a - self.p)

    def inter(self, l):
        '''
        当前线和另一条线的交点
        '''
        u = self.p - l.p
        denom = self.v ^ l.v
        if abs(denom) <= eps:  # Parallel lines
            return None
        t = (l.v ^ u) / denom
        return self.p + self.v * t

    def dis(self, a: Point):
        '''
        点到线段距离
        '''
        return abs((self.p - a) ^ self.v) / self.v.len()

class Segment:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b

    def is_on(self, p):
        '''
        判断p是否在线段上
        '''
        if self.a == p or self.b == p:
            return True
        return abs((p - self.a) ^ (p - self.b)) <= eps and ((p - self.a) * (p - self.b) < 0)

    def is_inter_line(self, l: Line):
        '''
        当前线段是否与 直线l 相交
        '''
        if l.toleft(self.a) == 0 or l.toleft(self.b) == 0:
            return True
        return l.toleft(self.a) != l.toleft(self.b)

    def is_inter_segment(self, s):
        '''
        当前线段是否与 线段s 相交
        '''
        if self.is_on(s.a) or self.is_on(s.b) or s.is_on(self.a) or s.is_on(self.b):
            return True
        l1 = Line(self.a, self.b - self.a)
        l2 = Line(s.a, s.b - s.a)
        return l1.toleft(s.a) * l1.toleft(s.b) == -1 and l2.toleft(self.a) * l2.toleft(self.b) == -1

    def dis_point(self, p: Point):
        '''
        当前线段与 点p 的最短距离
        '''
        if (p - self.a) * (self.b - self.a) < -eps or (p - self.b) * (self.a - self.b) < -eps:
            return min(p.dis(self.a), p.dis(self.b))
        l = Line(self.a, self.b - self.a)
        return l.dis(p)

    def dis_segment(self, s):
        '''
        当前线段与 线段s 的最短距离
        '''
        if self.is_inter_segment(s):
            return 0
        return min(self.dis_point(s.a), self.dis_point(s.b), s.dis_point(self.a), s.dis_point(self.b))

class Polygon:
    def __init__(self, points = None):
        '''
        端点
        '''
        if points is None:
            points = []
        self.points = points

    def nxt(self, i):
        '''
        后一条边
        '''
        return 0 if i == len(self.points) - 1 else i + 1

    def pre(self, i):
        '''
        前一条边
        '''
        return len(self.points) - 1 if i == 0 else i - 1

    def area(self):
        '''
        多边形面积
        '''
        res = 0
        for i in range(len(self.points)):
            res += self.points[i] ^ self.points[self.nxt(i)]
        return res / 2.0

    def is_convex(self):
        '''
        是不是凸多边形
        '''
        for i in range(len(self.points)):
            if (self.points[self.nxt(i)] - self.points[i]) ^ (self.points[self.pre(i)] - self.points[i]) < 0:
                return False
        return True

    def is_concave(self):
        '''
        是不是凹多边形
        '''
        if len(self.points) < 3:
            return False  # Not a valid polygon
        return not self.is_convex()

    def is_in(self, a):
        '''
        是不是在多边形内部
        0: 外部
        1: 边上
        2: 内部
        '''
        x = 0
        for i in range(len(self.points)):
            s = Segment(self.points[i], self.points[self.nxt(i)])
            if s.is_on(a):
                return 1
            p1 = self.points[i] - a
            p2 = self.points[self.nxt(i)] - a
            if p1.y > p2.y:
                p1, p2 = p2, p1
            if p1.y < eps < p2.y and (p1 ^ p2) > eps:
                x ^= 1
        return 2 if x else 0

    def winding(self, a):
        x = 0
        for i in range(len(self.points)):
            s = Segment(self.points[i], self.points[self.nxt(i)])
            if s.is_on(a):
                return -1e9
            p1 = self.points[i] - a
            p2 = self.points[self.nxt(i)] - a
            flag = False
            if p1.y > p2.y:
                p1, p2 = p2, p1
                flag = True
            if p1.y < eps < p2.y and (p1 ^ p2) > eps:
                if flag:
                    x -= 1
                else:
                    x += 1
        return x


# @TIME
def solve(testcase):
    n = II()
    points = []

    for _ in range(n):
        x, y = MI()
        points.append(Point(x, y))

    polygon = Polygon(points)
    print("Yes" if polygon.is_concave() else "No")

for testcase in range(1):
    solve(testcase)