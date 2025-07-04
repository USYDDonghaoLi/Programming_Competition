def centroid_finder(to, root=0):
    centroids = []
    pre_cent = []
    # subtree_size = []
    n = len(to)
    roots = [(root, -1, 1)]
    size = [1]*n
    is_removed = [0]*n
    parent = [-1]*n
    while roots:
        root, pc, update = roots.pop()
        parent[root] = -1
        if update:
            stack = [root]
            dfs_order = []
            while stack:
                u = stack.pop()
                size[u] = 1
                dfs_order.append(u)
                for v in to[u]:
                    if v == parent[u] or is_removed[v]: continue
                    parent[v] = u
                    stack.append(v)
            for u in dfs_order[::-1]:
                if u == root: break
                size[parent[u]] += size[u]
        c = root
        while 1:
            mx, u = size[root]//2, -1
            for v in to[c]:
                if v == parent[c] or is_removed[v]: continue
                if size[v] > mx: mx, u = size[v], v
            if u == -1: break
            c = u
        centroids.append(c)
        pre_cent.append(pc)
        # subtree_size.append(size[root])
        is_removed[c] = 1
        for v in to[c]:
            if is_removed[v]: continue
            roots.append((v, c, v == parent[c]))
    return centroids, pre_cent

from sys import stdin
input=lambda :stdin.readline()[:-1]

n=int(input())

graph = [[] for _ in range(n)]
for _ in range(n - 1):
    u,v=map(lambda x:int(x)-1,input().split())
    graph[u].append(v)
    graph[v].append(u)

cc,pp=centroid_finder(graph)

ans=[-1]*n
for i in range(1,n):
  ans[cc[i]]=pp[i]+1

print(*ans)