from typing import List

class Solution:
    def partitionString(self, s: str) -> List[str]:
        S = set()
        l, r = 0, 0
        res = []
        n = len(s)

        while r < n:
            while r < n and s[l: r + 1] in S:
                r += 1
            
            if s[l: r + 1] not in S:
                S.add(s[l: r + 1])
                res.append(s[l: r + 1])
                r += 1
                l = r
            else:
                break
        
        return res