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

# @TIME
def solve(testcase):
    n, L, R = MI()
    A = LII()

    damage_count = R - L + 1
    probability = 1.0 / damage_count

    max_health = max(A)

    """
    value[x][y] 表示：

    当前轮到行动的玩家，面对血量分别为 x 和 y 的怪物时，
    最终获胜的最大概率。

    游戏对两只怪物完全对称，因此：

        value[x][y] = value[y][x]

    prefix[x][y + 1] - prefix[x][y]
    就是 value[x][y]。

    prefix[x][k] =
        value[x][0] + value[x][1] + ... + value[x][k - 1]
    """
    prefix = [[0 for _ in range(A + 10)] for _ in range(A + 10)]

    # 只计算 x <= y 的一半状态。
    for x in range(max_health + 1):
        row_x = prefix[x]

        for y in range(x, max_health + 1):
            row_y = prefix[y]

            if x == 0 and y == 0:
                win = 0.0

            else:
                win_attack_x = -1.0
                win_attack_y = -1.0

                # 攻击第一只怪物，要求 x > 0。
                if x > 0:
                    lose_sum = 0.0

                    """
                    攻击后第一只怪物仍然存活：

                        remaining = x - damage > 0

                    remaining 的范围为：

                        max(1, x-R) ... x-L
                    """
                    low = x - R

                    if low < 1:
                        low = 1

                    high = x - L

                    if low <= high:
                        # value[z][y] = value[y][z]
                        lose_sum += (
                            row_y[high + 1] - row_y[low]
                        )

                    """
                    造成击杀的伤害满足：

                        damage >= x

                    每一种击杀伤害都会转移到状态 (0, y)。
                    """
                    first_killing_damage = x

                    if first_killing_damage < L:
                        first_killing_damage = L

                    if first_killing_damage <= R:
                        kill_count = (
                            R - first_killing_damage + 1
                        )

                        # value[0][y] = value[y][0]
                        lose_sum += kill_count * row_y[1]

                    win_attack_x = (
                        1.0 - lose_sum * probability
                    )

                # 攻击第二只怪物，要求 y > 0。
                if y > 0:
                    lose_sum = 0.0

                    low = y - R

                    if low < 1:
                        low = 1

                    high = y - L

                    if low <= high:
                        lose_sum += (
                            row_x[high + 1] - row_x[low]
                        )

                    first_killing_damage = y

                    if first_killing_damage < L:
                        first_killing_damage = L

                    if first_killing_damage <= R:
                        kill_count = (
                            R - first_killing_damage + 1
                        )

                        # value[x][0]
                        lose_sum += kill_count * row_x[1]

                    win_attack_y = (
                        1.0 - lose_sum * probability
                    )

                if x == 0:
                    # 第一只怪物已死亡，只能攻击第二只。
                    win = win_attack_y

                elif y == 0:
                    # 理论上在 x <= y 的循环中只有 (0,0)。
                    win = win_attack_x

                else:
                    # 当前玩家选择获胜概率更高的攻击目标。
                    win = fmax(win_attack_x, win_attack_y)

                # 避免浮点累计误差使概率略微越界。
                if win < 0.0:
                    win = 0.0
                elif win > 1.0:
                    win = 1.0

            # 写入 value[x][y] 的行前缀和。
            row_x[y + 1] = row_x[y] + win

            if x != y:
                # 根据对称性写入 value[y][x]。
                row_y[x + 1] = row_y[x] + win

    """
    开局过程：

    1. 托姆选择一只怪物，最大化自己的获胜概率；
    2. 汤姆从剩余怪物中选择一只，最小化托姆的获胜概率。

    因此答案为：

        max_i min_{j != i} value[h[i]][h[j]]
    """

    health_count = Counter(A)
    different_health = list(health_count.keys())

    answer = 0.0

    # 相同血量的怪物具有相同的选择结果，因此只枚举不同血量。
    for chosen_health in different_health:
        row = prefix[chosen_health]
        worst_probability = 1.0

        for opponent_health in different_health:
            """
            如果某种血量只有一只怪物，并且已经被托姆选择，
            汤姆就不能再次选择这只怪物。

            如果该血量出现至少两次，则汤姆仍然可以选择另一只
            相同血量的怪物。
            """
            if (
                opponent_health == chosen_health
                and health_count[chosen_health] == 1
            ):
                continue

            win_probability = (
                row[opponent_health + 1]
                - row[opponent_health]
            )

            if win_probability < worst_probability:
                worst_probability = win_probability

        if worst_probability > answer:
            answer = worst_probability

    print(f"{answer:.10f}")

for testcase in range(1):
    solve(testcase)