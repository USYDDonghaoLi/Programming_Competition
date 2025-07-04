queries = 0
def ask(i, x):
	global queries
	queries += 1
	assert queries <= 100000
	print(i, x)
	mx = int(input())
	assert mx != -1
	if mx == 0:
		print(0)
		correct = int(input())
		assert correct == 1
		exit(0)
	return mx

n = int(input())
mx = ask(1, 0)
zero = [0]*(n+1)

import random
if mx == 2**30 - 1:
	x = random.randint(0, 2**30 - 1)
	for i in range(1, n+1):
		newmx = ask(i, x)
		if newmx > mx:
			mx = ask(i, newmx)
			zero[i] = 1
		elif newmx < mx:
			mx = ask(i, mx ^ x)
			zero[i] = 1
	assert mx != 2**30 - 1

for bit in range(30):
	x = 1 << bit
	for i in range(1, n+1):
		if zero[i] == 1: continue
		newmx = ask(i, x)
		if newmx > mx:
			mx = ask(i, newmx)
			zero[i] = 1
		elif newmx < mx:
			mx = ask(i, mx ^ x)
			zero[i] = 1



