import sys

MAXN = 200010
parent = [0] * MAXN
rankk = [0] * MAXN
xor_to_par = [0] * MAXN
vis = [0] * MAXN
cur_version = 0

def findd(u):
    global cur_version
    if vis[u] != cur_version:
        parent[u] = u
        rankk[u] = 0
        xor_to_par[u] = 0
        vis[u] = cur_version
    if parent[u] != u:
        print(parent[u], u, 'abcabc')
        p, x = findd(parent[u])
        xor_to_par[u] ^= x
        parent[u] = p
    return parent[u], xor_to_par[u]

input = sys.stdin.read
data = input().split()

index = 0
T = int(data[index])
index += 1

for t in range(T):
    cur_version += 1
    n = int(data[index])
    index += 1
    m = int(data[index])
    index += 1
    has_conflict = False
    for _ in range(m):
        x = int(data[index])
        index += 1
        y = int(data[index])
        index += 1
        v = int(data[index])
        index += 1
        u = x
        vv = y + n
        pu, xu = findd(u)
        pv, xv = findd(vv)
        print(pu, xu, pv, xv)
        if pu == pv:
            implied = xu ^ xv
            if implied != v:
                has_conflict = True
        else:
            pu_temp, pv_temp = pu, pv
            xu_temp, xv_temp = xu, xv
            if rankk[pu_temp] > rankk[pv_temp]:
                pu_temp, pv_temp = pv_temp, pu_temp
                xu_temp, xv_temp = xv_temp, xu_temp
            print('wtf', pu_temp, pv_temp)
            parent[pu_temp] = pv_temp
            xor_to_par[pu_temp] = xu_temp ^ xv_temp ^ v
            if rankk[pu_temp] == rankk[pv_temp]:
                rankk[pv_temp] += 1
            print('xy', pu_temp, pv_temp)
        print("NO" if has_conflict else "YES")