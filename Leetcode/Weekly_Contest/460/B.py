fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

class Solution:
    def numOfSubsequences(self, s: str) -> int:
        res = 0
        s = s.lower()

        l, lc, lct = 1, 0, 0

        for c in s:
            if c == 'l':
                l += 1
            elif c == 'c':
                lc += l
            elif c == 't':
                lct += lc
            # print(l, lc, lct)

        res = fmax(res, lct)

        l, lc, lct = 0, 0, 0

        for c in s:
            if c == 'l':
                l += 1
            elif c == 'c':
                lc += l
            elif c == 't':
                lct += lc

        lct += lc

        res = fmax(res, lct)

        l, lc, lct = 0, 0, 0

        for c in s:
            if c == 'l':
                l += 1
            elif c == 'c':
                lc += l
            elif c == 't':
                lct += lc

        l = 0
        t = s.count('t')

        for c in s:
            res = fmax(res, lct + l * t)
            if c == 'l':
                l += 1
            if c == 't':
                t -= 1
            res = fmax(res, lct + l * t)

        return res