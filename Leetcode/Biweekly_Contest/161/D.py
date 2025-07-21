def popcount(n: int) -> int:
    n -= ((n >> 1) & 0x5555555555555555)
    n = (n & 0x3333333333333333) + ((n >> 2) & 0x3333333333333333)
    n = (n + (n >> 4)) & 0x0f0f0f0f0f0f0f0f
    n += ((n >> 8) & 0x00ff00ff00ff00ff)
    n += ((n >> 16) & 0x0000ffff0000ffff)
    n += ((n >> 32) & 0x00000000ffffffff)
    return n & 0x7f

C = [[0 for _ in range(51)] for _ in range(51)]
for i in range(51):
    C[i][0] = 1

for i in range(1, 51):
    for j in range(1, i + 1):
        C[i][j] = C[i - 1][j] + C[i - 1][j - 1]

from collections import *
from functools import *

class Solution:
    def popcountDepth(self, n: int, k: int) -> int:
        '''
        At most 50
        '''

        if k == 0:
            return 1

        q = deque()
        q.append(1)
        vis = [False for _ in range(51)]
        vis[1] = True

        for _ in range(k - 1):
            for __ in range(len(q)):
                cur = q.popleft()
                for i in range(51):
                    if popcount(i) == cur and not vis[i]:
                        vis[i] = True
                        q.append(i)

        # print('q', q)

        res = 0

        n = bin(n)[2:]
        m = len(n)

        @cache
        def dfs(cur, left, isStart, isLim):
            if cur == m:
                if not left:
                    return 1
                else:
                    return 0

            if left > m - cur:
                return 0

            if not left:
                # print('ONE!!!', cur, left, isStart, isLim)
                return 1

            ans = 0
            if isStart:
                if isLim:
                    if n[cur] == '0':
                        ans += dfs(cur + 1, left, True, True)
                    else:
                        ans += dfs(cur + 1, left, True, False)
                        if left:
                            ans += dfs(cur + 1, left - 1, True, True)
                else:
                    ans += C[m - cur][left]
            else:
                if cur == 0:
                    if left:
                        ans += dfs(cur + 1, left - 1, True, True)
                    # print('ans1', ans)
                    ans += dfs(cur + 1, left, False, False)
                    # print('ans2', ans)
                else:
                    ans += C[m - cur][left]
                    # print(m - cur, left, C[m - cur][left])

            # print('dfs', cur, left, isStart, isLim, ans)
            return ans
        
        res = 0
        for ele in q:
            res += dfs(0, ele, False, False)
            # print('ele', ele, dfs(0, ele, False, False))

        # print('res', res)

        if k == 1:
            res -= 1

        # else:
        #     q = deque()
        #     q.append(1)
        #     vis = [False for _ in range(51)]
        #     vis[1] = True
    
        #     for _ in range(k - 2):
        #         for __ in range(len(q)):
        #             cur = q.popleft()
        #             for i in range(51):
        #                 if popcount(i) == cur and not vis[i]:
        #                     vis[i] = True
        #                     q.append(i)

        #     for ele in q:
        #         res -= dfs(0, ele, False, False)
    
        return res