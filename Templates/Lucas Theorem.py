#when n>p
from functools import lru_cache
MOD=131
@lru_cache(None)
def factorial(n):
    return 1 if n==0 else n*factorial(n-1)
@lru_cache(None)
def inv(n):
    return pow(factorial(n),MOD-2,MOD)
def binom(n,m):
    return factorial(n)*inv(m)*inv(n-m)%MOD if n>=m else 0
def lucas(n,m):
    return binom(n%MOD,m%MOD)*binom(n//MOD,m//MOD) if n>MOD and m>MOD else binom(n,m)