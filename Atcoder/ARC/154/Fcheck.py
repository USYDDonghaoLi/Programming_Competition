from functools import *

mod = 998244353

@lru_cache(None)
def dfs(i, state):
    if state == (1 << i) - 1:
        return 0
    else:
        yes, no = 0, 0
        ret = 0
        for bit in range(i):
            if state >> bit & 1:
                yes += 1
            else:
                no += 1
                ret += (dfs(i, state | (1 << bit)) + 1) * pow(i, mod - 2, mod)
        ret = (ret + yes * pow(i, mod - 2, mod)) * i * pow(no, mod - 2, mod) % mod
        #print(state, ret, yes, no)
        return ret

for i in range(1, 11):
    print(i, dfs(i, 0))