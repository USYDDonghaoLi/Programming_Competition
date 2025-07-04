mod = 1000000007
eps = 10**-9


def main():
    import sys
    from collections import deque
    input = sys.stdin.readline

    N = int(input())
    adj = [[] for _ in range(N+1)]
    for _ in range(N-1):
        a, b = map(int, input().split())
        adj[a].append(b)
        adj[b].append(a)

    que = deque()
    que.append(1)
    seen = [-1] * (N+1)
    seen[1] = 0
    par = [0] * (N+1)
    child = [[] for _ in range(N+1)]
    seq = []
    while que:
        v = que.popleft()
        seq.append(v)
        for u in adj[v]:
            if seen[u] == -1:
                seen[u] = seen[v] + 1
                par[u] = v
                child[v].append(u)
                que.append(u)
    seq.reverse()

    used = [0] * (N+1)
    pair = [-1] * (N+1)
    for v in seq:
        if v == 1:
            continue
        p = par[v]
        if not used[p] and not used[v]:
            used[p] = 1
            used[v] = 1
            pair[p] = v
            pair[v] = p
    ans = 0
    seq.reverse()
    for v in seq:
        if not used[v]:
            ans += 1
        else:
            p = pair[v]
            for u in adj[p]:
                if not used[u]:
                    ans += 1
                    used[v] = 0
                    break
    print(ans)


if __name__ == '__main__':
    main()
