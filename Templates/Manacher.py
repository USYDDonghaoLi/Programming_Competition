def manacher(string):
    new_string =['', '$']
    for s in string:
        new_string.append(s)
        new_string.append('$')
    n = len(new_string)

    D =[0 for _ in range(n)]
    l, r = 0, 0

    for i in range(n):
        if i > r:
            while i - D[i] >= 0 and i + D[i] <n and new_string[i - D[i]] == new_string[i + D[i]]:
                D[i] += 1
            l, r = i - D[i] + 1, i + D[i] - 1

        else:
            j = l + r - i
            if j - D[j] >= l:
                D[i] = D[j]
            else:
                D[i] = j - l + 1
                while i - D[i] >= 0 and i + D[i] < n and new_string[i - D[i]] == new_string[i + D[i]]:
                    D[i] += 1
                l, r = i - D[i] + 1, i + D[i] - 1
    
    '''
    if i & 1:
        LEN = (v + 1 >> 1) * 2 - 1
    else:
        LEN = v >> 1 << 1    
    '''

    return D