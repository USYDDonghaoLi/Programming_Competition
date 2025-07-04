from random import *
from itertools import permutations
fo = open("Codeforces/Div.1 + 2/Round #854/in.txt", "w")
fo2 = open("Codeforces/Div.1 + 2/Round #854/out.txt", "w")
fo.write("10\n")
for _ in range(10):
    n = randint(1, 10)
    s = [chr(97 + randint(0, 5)) for _ in range(n)]
    fo.write(''.join(s) + "\n")
    res = 'z' * n
    for p in permutations(s):
        res = min(res, max(''.join(p), ''.join(p[::-1])))
    fo2.write(res + "\n")
fo.close()
fo2.close()