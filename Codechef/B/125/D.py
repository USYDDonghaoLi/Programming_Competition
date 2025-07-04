def pre_xor(n):
    if n%4 == 0: return n
    if n%4 == 1: return 1
    if n%4 == 2: return n+1
    return 0
def prepre_xor(n):
    if n%8 <= 1: return n
    if n%8 <= 3: return 2
    if n%8 <= 5: return n+2
    return 0
def range_prexor(l, r):
    if l == 0: return prepre_xor(r)
    return prepre_xor(r) ^ prepre_xor(l-1)
def calc(n, m):
    if min(n, m) <= 0: return 0
    res = range_prexor(2+m-1, n+m)
    res ^= range_prexor(1, n)
    return res

for _ in range(int(input())):
    n, m, x, y = map(int, input().split())
    ans = pre_xor(x-1) ^ pre_xor(y-1) ^ pre_xor(n-x) ^ pre_xor(m-y)
    for N in [x-1, n-x]:
        for M in [y-1, m-y]:
            ans ^= calc(N, M)
    print(ans)