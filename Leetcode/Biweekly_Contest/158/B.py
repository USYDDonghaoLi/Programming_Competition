from typing import *

inf = float('inf')

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

class Solution:
    def maximumProfit(self, A: List[int], k: int) -> int:
        n = len(A)

        '''
        0: no stock
        1: holding stock
        2: short-selling stock

        dp: maximum profit
        '''
        
        dp = [[[-inf for _ in range(3)] for _ in range(k + 1)] for _ in range(n + 1)]
        dp[0][0][0] = 0

        for day in range(1, n + 1):
            for lim in range(k + 1):
                '''
                no stock
                buy back
                sell
                '''
                dp[day][lim][0] = fmax(dp[day - 1][lim][0], fmax(dp[day - 1][lim][1] + A[day - 1], dp[day - 1][lim][2] - A[day - 1]))
                '''
                hold now or hold before
                '''
                if lim:
                    dp[day][lim][1] = fmax(dp[day - 1][lim][1], dp[day - 1][lim - 1][0] - A[day - 1])
                else:
                    dp[day][lim][1] = dp[day - 1][lim][1]

                '''
                short sell now or short sell before
                '''
                if lim:
                    dp[day][lim][2] = fmax(dp[day - 1][lim][2], dp[day - 1][lim - 1][0] + A[day - 1])
                else:
                    dp[day][lim][2] = dp[day - 1][lim][2]

        res = 0
        for lim in range(k + 1):
            res = fmax(res, dp[n][lim][0])

        return res