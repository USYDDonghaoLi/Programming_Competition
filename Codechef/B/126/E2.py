def dfs(graph, start=0):
    n = len(graph)
    order = []
    visited, parent = [False] * n, [-1] * n

    stack = [start]
    while stack:
        start = stack[-1]
        stack.pop()

        visited[start] = True
        order.append(start)
        for child in graph[start]:
            if not visited[child]:
                parent[child] = start
                stack.append(child)

    return parent, order

for _ in range(int(input())):
    n = int(input())
    gr = [ [] for _ in range(n) ]
    for i in range(n-1):
        u, v = map(int, input().split())
        gr[u-1].append(v-1)
        gr[v-1].append(u-1)
    parent, order = dfs(gr)

    subsz = [0]*n
    for u in reversed(order):
        subsz[u] += 1
        if u > 0: subsz[parent[u]] += subsz[u]
    print(subsz)
    
    within = [0]*n
    through = [0]*n
    ans = 0
    for u in range(n):
        through[u] = n*(n-1)//2
        through[u] -= (n - subsz[u]) * (n - subsz[u] - 1) // 2

        within[u] = subsz[u]*(subsz[u] - 1) // 2
        for v in gr[u]:
            if parent[v] == u:
                through[u] -= subsz[v] * (subsz[v] - 1) // 2
                within[u] -= subsz[v] * (subsz[v] - 1) // 2
    print(through)
    print(within)
    
    for u in range(n):
        ans += within[u] * (n - subsz[u]) * (n - subsz[u] - 1) // 2
        if u > 0:
            ans += (through[parent[u]] - (subsz[u] * (n - subsz[u]))) * subsz[u] * (subsz[u] - 1) // 2
    print(ans // 2)