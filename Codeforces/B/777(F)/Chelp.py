nums = [2]
for i in range(3, 10 ** 5, 2):
    flag = True
    for j in range(3, int(i **.5) + 1):
        if i % j == 0:
            flag = False
            break
    if flag:
        nums.append(i)
print(nums)