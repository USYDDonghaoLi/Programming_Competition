res = 0
S = set()
for i in range(1, 8):
    for j in range(1, 8):
        for k in range(1, 8):
            s = sorted([i, j, k])
            a, b, c = s
            if a + b > c and c - b < a:
                S.add(tuple(s))
print(len(S))
print(S)