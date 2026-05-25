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
def LGMI():
    return list(map(lambda x: int(x) - 1, input().split()))

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
from typing import List, Optional

eps = 1e-9

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        return abs(self.x - other.x) <= eps and abs(self.y - other.y) <= eps

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __mul__(self, other):
        """支持数乘和点积"""
        if isinstance(other, Point):
            return self.x * other.x + self.y * other.y          # 点积
        return Point(self.x * other, self.y * other)            # 数乘

    def __truediv__(self, k: float):
        return Point(self.x / k, self.y / k)

    def __xor__(self, other):                                   # 叉积
        return self.x * other.y - self.y * other.x

    def dot(self, other) -> float:                              # 显式点积
        return self.x * other.x + self.y * other.y

    def cross(self, other) -> float:                            # 显式叉积
        return self.x * other.y - self.y * other.x

    def toleft(self, other) -> int:
        """当前点相对于other的位置：1=左，-1=右，0=共线"""
        t = self.cross(other)
        return (t > eps) - (t < -eps)

    def len2(self) -> float:
        return self * self

    def len(self) -> float:
        return math.sqrt(self.len2())

    def dis2(self, other) -> float:
        return (other - self).len2()

    def dis(self, other) -> float:
        return math.sqrt(self.dis2(other))

    def rotate(self, alpha: float):
        """逆时针旋转 alpha 弧度"""
        return Point(
            self.x * math.cos(alpha) - self.y * math.sin(alpha),
            self.x * math.sin(alpha) + self.y * math.cos(alpha),
        )

    def normalize(self):
        """单位向量"""
        length = self.len()
        return self / length if length > eps else Point(0, 0)

    def perpendicular(self):
        """垂直向量（逆时针 90 度）"""
        return Point(-self.y, self.x)

    def angle(self) -> float:
        """极角（atan2）"""
        return math.atan2(self.y, self.x)


class Line:
    def __init__(self, p: Point, v: Point):
        self.p = p
        self.v = v

    def toleft(self, a: Point) -> int:
        return self.v.toleft(a - self.p)

    def inter(self, l) -> Optional[Point]:
        """两条直线交点，平行返回 None"""
        d = self.v.cross(l.v)
        if abs(d) < eps:
            return None
        u = self.p - l.p
        t = (l.v.cross(u)) / d
        return self.p + self.v * t

    def projection(self, a: Point) -> Point:
        """点 a 在直线上的投影"""
        t = ((a - self.p) * self.v) / (self.v * self.v)
        return self.p + self.v * t

    def dis(self, a: Point) -> float:
        """点到直线距离"""
        return abs((self.p - a).cross(self.v)) / self.v.len()


class Segment:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b

    def is_on(self, p: Point) -> bool:
        if self.a == p or self.b == p:
            return True
        return abs((p - self.a).cross(p - self.b)) < eps and (p - self.a) * (p - self.b) < 0

    def is_inter_line(self, l: Line) -> bool:
        if abs(l.toleft(self.a)) == 0 or abs(l.toleft(self.b)) == 0:
            return True
        return l.toleft(self.a) * l.toleft(self.b) == -1

    def is_inter_segment(self, s) -> bool:
        if self.is_on(s.a) or self.is_on(s.b) or s.is_on(self.a) or s.is_on(self.b):
            return True
        l1 = Line(self.a, self.b - self.a)
        l2 = Line(s.a, s.b - s.a)
        return l1.toleft(s.a) * l1.toleft(s.b) == -1 and l2.toleft(self.a) * l2.toleft(self.b) == -1

    def dis_point(self, p: Point) -> float:
        if (p - self.a) * (self.b - self.a) < -eps or (p - self.b) * (self.a - self.b) < -eps:
            return min(p.dis(self.a), p.dis(self.b))
        l = Line(self.a, self.b - self.a)
        return l.dis(p)

    def dis_segment(self, s) -> float:
        if self.is_inter_segment(s):
            return 0
        return min(self.dis_point(s.a), self.dis_point(s.b),
                   s.dis_point(self.a), s.dis_point(self.b))


class Polygon:
    def __init__(self, points: List[Point] = None):
        self.points = points or []

    def nxt(self, i: int) -> int:
        return 0 if i == len(self.points) - 1 else i + 1

    def pre(self, i: int) -> int:
        return len(self.points) - 1 if i == 0 else i - 1

    def area(self) -> float:
        res = 0.0
        for i in range(len(self.points)):
            res += self.points[i].cross(self.points[self.nxt(i)])
        return res / 2.0

    def is_convex(self) -> bool:
        for i in range(len(self.points)):
            if (self.points[self.nxt(i)] - self.points[i]).cross(
                    self.points[self.pre(i)] - self.points[i]) < -eps:
                return False
        return True

    def is_in(self, a: Point) -> int:
        """
        返回值说明：
            0 : 严格在多边形外部
            1 : 在边界上
            2 : 严格在多边形内部
        """
        if not self.points:
            return 0
        x = 0
        for i in range(len(self.points)):
            s = Segment(self.points[i], self.points[self.nxt(i)])
            if s.is_on(a):
                return 1
            p1 = self.points[i] - a
            p2 = self.points[self.nxt(i)] - a
            if p1.y > p2.y:
                p1, p2 = p2, p1
            if p1.y < eps < p2.y and p1.cross(p2) > eps:
                x ^= 1
        return 2 if x else 0

    def winding(self, a: Point) -> float:
        """Winding number（可用于有向多边形）"""
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
            if p1.y < eps < p2.y and p1.cross(p2) > eps:
                x += -1 if flag else 1
        return x


# ====================== 常用辅助函数 ======================

def convex_hull(points: List[Point]) -> Polygon:
    """Andrew 单调栈求凸包（O(n log n)）"""
    if len(points) <= 1:
        return Polygon(points[:])
    points = sorted(points, key=lambda p: (p.x, p.y))
    lower, upper = [], []
    for p in points:
        while len(lower) >= 2 and (lower[-1] - lower[-2]).cross(p - lower[-2]) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper) >= 2 and (upper[-1] - upper[-2]).cross(p - upper[-2]) <= 0:
            upper.pop()
        upper.append(p)
    hull = lower[:-1] + upper[:-1]
    return Polygon(hull)


def polar_sort(points: List[Point], origin: Point = None) -> List[Point]:
    """以 origin 为极点按极角排序（默认取最左下点）"""
    if origin is None:
        origin = min(points, key=lambda p: (p.y, p.x))
    def key(p):
        return (p - origin).angle(), (p - origin).len2()
    return sorted(points, key=key)


class Circle:
    def __init__(self, center: Point, radius: float):
        self.c = center
        self.r = radius

    def area(self) -> float:
        return math.pi * self.r * self.r

    def contain_point(self, p: Point) -> int:
        d = p.dis(self.c)
        if abs(d - self.r) < eps:
            return 1  # 边界
        return 2 if d < self.r else 0  # 内部 / 外部

# @TIME
def solve(testcase):
    n = II()
    A = []

    for _ in range(3 * n):
        x, y = MI()
        A.append(Point(x, y))
    
    def check_line(line):
        """Check if a line separates exactly n points to left and n to right"""
        left, on, right = 0, 0, 0
        for k in range(3 * n):
            if line.toleft(A[k]) > 0:
                left += 1
            elif line.toleft(A[k]) < 0:
                right += 1
            else:
                on += 1
        if left == n and right == n:
            a = line.v.y
            b = -line.v.x
            c = -(a * line.p.x + b * line.p.y)
            if a < 0:
                a, b, c = -a, -b, -c
            elif a == 0 and b < 0:
                b, c = -b, -c
            print(a, b, c)
            assert abs(a) <= 10 ** 18 and abs(b) <= 10 ** 18 and abs(c) <= 10 ** 18
            return True
        return False
    
    for i in range(3 * n):
        for j in range(i + 1, 3 * n):
            if A[i] == A[j]:
                continue
            line = Line(A[i], A[j] - A[i])
            if check_line(line):
                return
    
    for i in range(3 * n):
        for j in range(i + 1, 3 * n):
            if A[i] == A[j]:
                continue
            direction = A[j] - A[i]
            perpendicular = direction.perpendicular()
            # Try perpendicular direction through all points
            for k in range(3 * n):
                line = Line(A[k], perpendicular)
                if check_line(line):
                    return
    
    print(-1)

for testcase in range(1):
    solve(testcase)