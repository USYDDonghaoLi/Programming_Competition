import random
S = [1]
with open('P:\Algothrim\Codeforces\Div. 2\Round #774\Dhelp.txt', 'w') as f:
    f.write('200000')
    f.write('\n')
    adj = []
    for i in range(2, 200001):
        f.seek(0, 1)
        idx = random.randint(0, i - 2)
        adj.append(str(S[idx]) + ' ' + str(i))
        S.append(i)
    random.shuffle(adj)
    for item in adj:
        f.write(item + '\n')

f.close()
