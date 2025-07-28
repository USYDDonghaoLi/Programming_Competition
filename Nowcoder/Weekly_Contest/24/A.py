n = int(input())
res = [[-1 for _ in range(n)] for _ in range(n)]

cur = 1
for i in range(n):
    if i & 1:
        for j in range(n - 1, -1, -1):
            res[i][j] = cur
            cur += 1
    else:
        for j in range(n):
            res[i][j] = cur
            cur += 1

for i in range(n):
    print(*res[i])