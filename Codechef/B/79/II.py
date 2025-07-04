mod, maxn = 998244353, 2 * 10**6 + 20
fac = [1]
for i in range(1,  maxn):
	fac.append(i * fac[i-1] % mod)

ifac = fac[:]
ifac[-1] = pow(fac[-1], mod-2, mod)
for i in reversed(range(maxn-1)):
    ifac[i] = ifac[i+1] * (i+1) % mod

def C(n, r):
	if n < r or r < 0: return 0
	return fac[n] * ifac[r] * ifac[n-r] % mod

def f(n, k): # number of integer solutions to a1 + a2 + ... + an = k, each ai >= 0
	if n == 0: return 1 if k == 0 else 0
	return C(n+k-1, k)

for _ in range(int(input())):
	n, m, k = map(int, input().split())
	a = list(map(int, input().split()))
	base_ops = 0
	for i in range(k):
		cur = a[i::k]
		base_ops += len(cur) * max(cur) - sum(cur)
	if base_ops > m:
		print(0)
		continue
	m -= base_ops
	print('nmk', n, m, k)

	lo, hi, ct = n//k, (n+k-1)//k, (-n)%k
	ans = 0

	dp = [f(k - ct, 0)]
	for i in range(1, m+1):
		dp.append(dp[-1] + f(k - ct, i))
	print('dp', dp)
	
	for i in range(m // lo + 1):
		y = m - lo*i
		ans += f(ct, i) * dp[y // hi] % mod
	print(ans % mod)