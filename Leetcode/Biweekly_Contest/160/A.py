def f(num):

    res = []

    while num:
        t = num % 16
        # print('ft', t)
        if 0 <= t <= 9:
            res.append(str(t))
        else:
            res.append(chr(65 + t - 10))
        num = num // 16

    return ''.join(res[::-1])

def g(num):

    res = []

    while num:
        t = num % 36
        # print('gt', t)
        if 0 <= t <= 9:
            res.append(str(t))
        else:
            res.append(chr(65 + t - 10))
        num = num // 36

    return ''.join(res[::-1])


class Solution:
    def concatHex36(self, n: int) -> str:
        return f(n * n) + g(n * n * n)