import sys
from collections import defaultdict
from collections import deque
import bisect
input = sys.stdin.readline
import math


n = int(input())

e = []
for _ in range(n):
    x, y = map(float, input().split())
    e.append((x, y))

ans = 0
d = 0
ln2 = math.log(2)
eps = 1e-12
for i in range(1, len(e)):
    x1 = e[i][0];y1 = e[i][1]
    x2 = e[i - 1][0];y2 = e[i - 1][1]
    dx = x2 - x1
    dy = y2 - y1
    d1 = math.sqrt(dx * dx + dy * dy)

    num1 = d1 * ln2
    if num1 >= 1:
      k = math.log(num1, 2.0)
      print('k', k)
      ans += 2 * k + 2 / ln2
    else:
      ans += 2 * d1


print(ans)
































