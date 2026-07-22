from collections import defaultdict
import sys
input = sys.stdin.readline

n = int(input())
pts = [tuple(map(int, input().split())) for _ in range(n)]

mx = defaultdict(lambda: -10**18)
mn = defaultdict(lambda: 10**18)
ans = 0

for i in range(n):
    x1, y1 = pts[i]
    for j in range(i):
        x2, y2 = pts[j]
        dx, dy = x1 - x2, y1 - y2
        if dx > 0 or (dx == 0 and dy > 0):
            dx, dy = -dx, -dy
        s = dy * x1 - dx * y1
        key = (dx, dy)
        mx[key] = max(mx[key], s)
        mn[key] = min(mn[key], s)
        ans = max(ans, mx[key] - mn[key])

print(f"{ans}.0" if ans else -1)