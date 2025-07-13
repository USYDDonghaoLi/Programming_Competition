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

class Player:
    def __init__(self, name, v, draw_list):
        self.name = name
        self.health = v
        self.field = []
        self.draw = deque(draw_list)
        self.discard = deque()

    def move_discard_to_draw(self):
        if not self.draw and self.discard:
            self.draw = deque(self.discard)
            self.discard.clear()

    def group_damage(self, opponent, c):
        if not opponent.field:
            opponent.health -= c
            if opponent.health <= 0:
                return True
        else:
            for role in opponent.field:
                role[0] -= c
            new_field = []
            for role in opponent.field:
                if role[0] > 0:
                    new_field.append(role)
                else:
                    opponent.discard.append(role[2])
            opponent.field = new_field
        return opponent.health <= 0

    def settle_function(self, c, opponent):
        return self.group_damage(opponent, c)

    def attack_phase(self, opponent):
        for my_role in self.field[:]:
            if opponent.health <= 0:
                break
            if opponent.field:
                opp_role = opponent.field[0]
                opp_role[0] -= my_role[1]
                if opp_role[0] <= 0:
                    died = opponent.field.pop(0)
                    opponent.discard.append(died[2])
            else:
                opponent.health -= my_role[1]
                if opponent.health <= 0:
                    return True
        return opponent.health <= 0

# @TIME
def solve(testcase):
    n, m, v = MI()

    cards = [None for _ in range(n)]

    for i in range(n):
        cardInfo = LII()
        category = cardInfo[0]
        if category == 0:
            cards[i] = ('role', cardInfo[1], cardInfo[2])
        else:
            cards[i] = ('func', cardInfo[1])

    P = LII()
    Admin_cards = []

    for p in P:
        Admin_cards.append(cards[p - 1])
    
    Q = LII()
    SS_cards = []

    for q in Q:
        SS_cards.append(cards[q - 1])
    
    k = II()
    operations = [LII() for _ in range(k)]
    # for i in range(k):
    #     ops = operations[i]
    #     op = ops[0]

        # if op == 1:
        #     x = ops[1]
        #     operations.append((1, x))
        # else:
        #     operations.append((2))
    
    admin = Player('Administrator', v, Admin_cards)
    ss = Player('S.S.', v, SS_cards)

    winner = 'Draw'

    for turn in range(k):
        if winner != 'Draw':
            break

        if turn & 1:
            current = ss
            opponent = admin
        else:
            current = admin
            opponent = ss
        
        op, *args = operations[turn]
        win_after_op = None

        if op == 1:
            x = args[0]
            win_after_op = current.settle_function(x, opponent)
        elif op == 2:
            current.move_discard_to_draw()
            if current.draw:
                top_card = current.draw[0]
                if top_card[0] == 'func':
                    current.draw.popleft()
                    win_after_op = current.settle_function(top_card[1], opponent)
                    current.discard.append(top_card)
                elif top_card[0] == 'role' and len(current.field) < 10:
                    current.draw.popleft()
                    a, b = top_card[1], top_card[2]
                    current.field.append([a, b, top_card])
        
        if win_after_op:
            winner = current.name
            continue

        win_after_attack = current.attack_phase(opponent)
        if win_after_attack:
            winner = current.name
    
    print(winner)

for testcase in range(II()):
    solve(testcase)