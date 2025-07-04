#ABC378D

#入力受取・assert
H, W, K = map(int, input().split())
S = [input() for _ in range(H)]
assert 1 <= H <= 10 and 1 <= W <= 10
assert 1 <= K <= 11
free = False
for h in range(H):
    assert all(Shw in '.#' for Shw in S[h])
    free |= any(Shw == '.' for Shw in S[h])
assert free

#DFSで間に合うはず  一次元化する
G = [[] for _ in range(H * W)]
T = [S[h][w] == '#' for h in range(H) for w in range(W)]
for h in range(H):
    for w in range(W):
        if S[h][w] == '.':
            for x, y in [(h - 1, w), (h + 1, w), (h, w - 1), (h, w + 1)]:
                if x in range(H) and y in range(W) and S[x][y] == '.':
                    G[h * W + w].append(x * W + y)

ans = 0
visited = [False] * H * W
stack = [0] * 1000
for p in range(H * W):
    if T[p] == True: continue
    stack[ d := 0 ] = p
    depth = -1
    while d >= 0:
        now = stack[d]
        if now >= 0:
            depth += 1  #この時点で+1
            stack[d] = ~ now
            visited[now] = True
            if depth == K:
                ans += 1
                continue
            for nxt in G[now]:
                if visited[nxt] == False:
                    stack[ d := d + 1 ] = nxt
        else:
            now = ~ now
            depth -= 1
            d -= 1
            visited[now] = False
print(ans)
