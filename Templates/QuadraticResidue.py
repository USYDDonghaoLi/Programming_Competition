import random

p: int

class Complex:
    def __init__(self, a=0, b=0):
        self.a = a
        self.b = b

    def __mul__(self, other):
        if isinstance(other, Complex):
            a = (self.a * other.a % p + i2 * self.b * other.b % p) % p
            b = (self.b * other.a % p + self.a * other.b % p) % p
            return Complex(a, b)
        else:
            return Complex(self.a * other % p, self.b * other % p)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

def fpow(a, b):
    if isinstance(a, Complex):
        res = Complex(1, 0)
        while b:
            if b & 1:
                res = res * a
            a = a * a
            b >>= 1
        return res
    else:
        res = 1
        while b:
            if b & 1:
                res = res * a % p
            a = a * a % p
            b >>= 1
        return res

def check(x):
    return fpow(x, (p - 1) // 2) == p - 1

def out(x0, x1):
    if x0 > x1:
        x0, x1 = x1, x0
    if x0 != x1:
        print(x0, end=' ')
    print(x1)

def cipolla(a, p):
    global i2
    if a % p == 0:
        print(0)
        return
    if check(a):
        print("Hola!")
        return
    r = 0
    while True:
        r = random.randint(0, p - 1)
        i2 = (r * r % p - a) % p
        if r and check(i2):
            break
    x0 = (fpow(Complex(r, -1 + p), (p + 1) // 2).a) % p
    x1 = p - x0
    out(x0, x1)
    assert (x0 * x0 % p - a) % p == 0
    assert (x1 * x1 % p - a) % p == 0

# T = int(input())
# for _ in range(T):
#     a, p = map(int, input().split())
#     cipolla(a, p)