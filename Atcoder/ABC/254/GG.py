from bisect import bisect_left, bisect_right

n, m, Q = map(int, input().split())
elev = [[] for _ in range(n)]
for _ in range(m):
    a, b, c = map(int, input().split())
    elev[a - 1].append((b, c))

elevall = []
for i in range(n):
    if not elev[i]:
        continue
    elev[i].sort()
    ll, rr = elev[i][0]
    lst = []
    for l, r in elev[i][1:]:
        if l <= rr:
            rr = max(rr, r)
        else:
            lst.append((ll, rr))
            ll = l
            rr = r
    lst.append((ll, rr))
    elev[i] = []
    for l, r in lst:
        elev[i] += [l, r]
    elevall += lst[:]

elevall.sort()
ll, rr = elevall[0]
lst = []
se = {ll, rr}
for l, r in elevall[1:]:
    se.add(l)
    se.add(r)
    if l <= rr:
        rr = max(rr, r)
    else:
        lst += [ll, rr]
        ll = l
        rr = r
lst += [ll, rr]

llrr = sorted(se)
dic = {s:i for i, s in enumerate(llrr)}
le = len(se)
nex = [[-1] * le for _ in range(30)]
for l, r in elevall:
    r = dic[r]
    l = dic[l]
    nex[0][l] = max(nex[0][l], r)
for i in range(1, le):
    nex[0][i] = max(nex[0][i], nex[0][i - 1])
for i in range(1, 30):
    for j in range(le):
        nex[i][j] = nex[i - 1][nex[i - 1][j]]

bi = [1 << i for i in range(30)]

for _ in range(Q):
    x, y, z, w = map(int, input().split())
    if y == w:
        if x == z:
            print(0)
        else:
            print(1)
        continue
    if y > w:
        x, z = z, x
        y, w = w, y
    
    p1 = bisect_right(lst, y)
    p2 = bisect_left(lst, w)
    print(p1, p2)
    if p1 != p2 or not p1 & 1:
        print(-1)
        continue
    
    ans = w - y
    print('ans', ans)
    x -= 1
    z -= 1
    p = bisect_right(elev[x], y)
    if p & 1:
        y = elev[x][p]
        y = dic[y]
    else:
        y = bisect_right(llrr, y) - 1
    print('py1', p, y)
    p = bisect_left(elev[z], w)
    if p & 1:
        w = elev[z][p - 1]
        w = dic[w]
    else:
        w = bisect_left(llrr, w)
    print('py2', p, w)
    if w <= y:
        if x != z:
            ans += 1
        print(ans)
        continue

    
    cnt = 0
    for i in range(29, -1, -1):
        if nex[i][y] < w:
            ans += bi[i]
            y = nex[i][y]
        
    ans += 2
    print(ans)


