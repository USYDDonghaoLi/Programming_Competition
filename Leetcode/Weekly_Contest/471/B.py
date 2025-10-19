class Solution:
    def longestBalanced(self, s: str) -> int:
        n = len(s)
        s = [ord(c) - 97 for c in s]

        res = [[0 for _ in range(n + 1)] for _ in range(26)]

        for i, v in enumerate(s):
            for j in range(26):
                if j == v:
                    res[j][i + 1] = res[j][i] + 1
                else:
                    res[j][i + 1] = res[j][i]

        ans = 0

        for i in range(n):
            for j in range(i, n):
                flag = True
                freq = -1
                for k in range(26):
                    tmp = res[k][j + 1] - res[k][i]
                    if tmp:
                        if freq == -1:
                            freq = tmp
                        else:
                            if freq != tmp:
                                flag = False
                                break

                if flag:
                    ans = max(ans, j - i + 1)

        return ans