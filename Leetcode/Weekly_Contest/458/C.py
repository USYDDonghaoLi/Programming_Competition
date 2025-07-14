class Solution:
    def processStr(self, s: str, k: int) -> str:
        l = 0
        A = [0]
        for c in s:
            if c == '*':
                if l > 0:
                    l -= 1
            elif c == '#':
                l <<= 1
            elif c == '%':
                pass
            else:
                l += 1
            A.append(l)

        if k >= l:
            return '.'

        idx = len(A) - 1

        n = len(s)
        for i in range(n - 1, -1, -1):
            cur = A[idx]
            if s[i].isalpha():
                if k == cur - 1:
                    return s[i]
            elif s[i] == '%':
                prev = A[idx - 1]
                k = prev - 1 - k
            elif s[i] == '*':
                pass
            else:
                prev = A[idx - 1]
                if k <= prev - 1:
                    pass
                else:
                    k -= prev
            idx -= 1
            # print('ik', i, k)

        return 'fuck'