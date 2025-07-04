from heapq import *

def f(nums1, nums2, k):
    n = len(nums1)
    idxs = [i for i in range(n)]
    idxs.sort(key = lambda x: -nums2[x])

    pq = [] #最小堆#
    s = 0  #堆内元素和
    res = 0

    for i in idxs:
        s += nums1[i]
        heappush(pq, nums1[i])
        #堆内元素超过k就pop掉最小值#
        while len(pq) > k:
            s -= heappop(pq)
        if len(pq) == k:
            res = max(res, s * nums2[i])
        #print('pq', pq, nums2[i])
    
    return res

print(f([1, 3, 3, 2], [2, 1, 3, 4], 3))
print(f([4, 2, 3, 1, 1], [7, 5, 10, 9, 6], 1))