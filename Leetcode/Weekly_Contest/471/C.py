from collections import *

class Solution:
    def longestBalanced(self, s: str) -> int:
        n = len(s)

        res = 0

        l, r = 0, 0
        while r < n:
            while r < n and s[l] == s[r]:
                r += 1
            res = max(res, r - l)
            l = r

        def calc2(s, char):
            if not s:
                return 0
                
            alphabet = ['a', 'b', 'c']
            alphabet.remove(char)

            a, b = 0, 0
            mp = defaultdict(int)
            mp[0] = 0

            res = 0
            for i, c in enumerate(s, 1):
                if c == alphabet[0]:
                    a += 1
                else:
                    b += 1
                if a - b not in mp:
                    mp[a - b] = i
                else:
                    res = max(res, i - mp[a - b])

            return res
                

        for char in ('a', 'b', 'c'):
            for ss in s.split(char):
                res = max(res, calc2(ss, char))

        mp = defaultdict(int)

        a, b, c = 0, 0, 0
        mp[(0, 0)] = 0

        for i, char in enumerate(s, 1):
            if char == 'a':
                a += 1
            elif char == 'b':
                b += 1
            else:
                c += 1

            if (a - b, b - c) not in mp:
                mp[(a - b, b - c)] = i
            else:
                res = max(res, i - mp[(a - b, b - c)])

            # print('wtf', i, a - b, b - c)

        return res