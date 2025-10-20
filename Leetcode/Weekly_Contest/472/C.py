from collections import *

class Solution:
    def lexGreaterPermutation(self, s: str, t: str) -> str:
        s = [ord(c) - 97 for c in s]
        t = [ord(c) - 97 for c in t]
        n = len(s)
        res = [25 for _ in range(n + 1)]

        c = Counter(s)

        for i in range(n):
            char = t[i]
            tmp = t[:i]
            choice = -1
            for j in range(char + 1, 26):
                if c[j]:
                    choice = j
                    tmp.append(j)
                    break
            if choice != -1:
                for k in range(26):
                    if k == choice:
                        for _ in range(c[k] - 1):
                            tmp.append(k)
                    else:
                        for _ in range(c[k]):
                            tmp.append(k)
            # print(i, tmp, c, choice)
                if tmp != t:
                    res = min(res, tmp)

            if not c[char]:
                break
            else:
                c[char] -= 1

        res = ''.join([chr(c + 97) for c in res])
        
        if res == 'z' * (n + 1):
            return ''
        else:
            return res
                