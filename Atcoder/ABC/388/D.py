def solve():
    import sys

    input_data = sys.stdin.read().strip().split()
    N = int(input_data[0])
    A = list(map(int, input_data[1:]))
    
    i = 0
    j = (N + 1) // 2

    count = 0
    while i < (N + 1) // 2 and j < N:
        if 2 * A[i] <= A[j]:
            count += 1
            i += 1
            j += 1
        else:
            j += 1

    print(count)

solve()
