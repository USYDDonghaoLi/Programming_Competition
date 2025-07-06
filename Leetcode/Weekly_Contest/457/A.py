from typing import *
from collections import *

S = set()
for i in range(26):
    S.add(chr(65 + i))
    S.add(chr(97 + i))

for i in range(10):
    S.add(str(i))

S.add('_')

S2 = []
S2.append("electronics")
S2.append("grocery")
S2.append("pharmacy")
S2.append("restaurant")

class Solution:
    def validateCoupons(self, A: List[str], B: List[str], C: List[bool]) -> List[str]:
        mp = defaultdict(list)
        
        for a, b, c in zip(A, B, C):
            flag = True

            if not len(a):
                flag = False

            for aa in a:
                if aa not in S:
                    flag = False

            if b not in S2:
                flag = False

            if not c:
                flag = False

            if flag:
                mp[b].append(a)

        res = []
        for b in S2:
            mp[b].sort()
            res.extend(mp[b])

        return res