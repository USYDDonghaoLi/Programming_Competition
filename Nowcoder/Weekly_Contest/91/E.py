import sys
input = lambda:sys.stdin.readline()

def check1(arr,n,m):
    # 是否恰好（一行）两行为1，其余为0
    cnt = 0
    for i in range(n):
        row = arr[i]
        start = row[0]
        if start == '1':
            cnt += 1
        for j in range(1,m):
            if row[j] != start:
                return False
    return cnt == 0 or cnt == 2

def check2(arr,n,m):
    # 列
    cnt = 0
    for j in range(m):
        start = arr[0][j]
        if start == '1':
            cnt += 1
        for i in range(1,n):
            if arr[i][j] != start:
                return False
    return cnt == 0 or cnt == 2

def check3(arr,n,m):
    row = -1
    col = -1
    for i in range(n):
        cnt0 = 0
        for j in range(m):
            if arr[i][j] == '0':
                cnt0 += 1
        if cnt0 == 1:
            row = i
            break
    
    for j in range(m):
        cnt0 = 0
        for i in range(n):
            if arr[i][j] == '0':
                cnt0 += 1
        if cnt0 == 1:
            col = j
            break
    
    if col == -1 or row == -1:
        return False
    
    if arr[row][col] != '0':
        return False
    
    for i in range(n):
        for j in range(m):
            if i == row or j == col:
                continue
            if arr[i][j] == '1':
                return False
    return True
            
    


def solve():
    g = []
    n,m = map(int,input().split())
    for i in range(n):
        s = input()
        g.append(list(s))
#     print(check1(g,n,m),check2(g,n,m),check3(g,n,m))
    if check1(g,n,m):
        print('YES')
        return
    if check2(g,n,m):
        print('YES')
        return
    if check3(g,n,m):
        print('YES')
        return
    print('NO')

T = int(input())
for _ in range(T):
    solve()
        