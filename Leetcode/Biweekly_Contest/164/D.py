def popcount(n: int) -> int:
    n -= ((n >> 1) & 0x5555555555555555)
    n = (n & 0x3333333333333333) + ((n >> 2) & 0x3333333333333333)
    n = (n + (n >> 4)) & 0x0f0f0f0f0f0f0f0f
    n += ((n >> 8) & 0x00ff00ff00ff00ff)
    n += ((n >> 16) & 0x0000ffff0000ffff)
    n += ((n >> 32) & 0x00000000ffffffff)
    return n & 0x7f

from collections import deque

for n in range(1, 8):
    for m in range(1, n + 1):
        a = ((1 << n) - 1) ^ ((1 << m) - 1)
        # print(n, m, bin(cur)[2:])
        avail = [[] for _ in range(n + 1)]
        for state in range(1 << n):
            avail[popcount(state)].append(state)

        for k in range(1, n + 1):
            vis = [False for _ in range(1 << n)]
            q = deque()
            vis[a] = True
            q.append(a)

            while q:
                cur = q.popleft()
                for s in avail[k]:
                    ns = cur ^ s
                    if not vis[ns]:
                        vis[ns] = True
                        q.append(ns)

            print(n, m, k, vis[-1]) 