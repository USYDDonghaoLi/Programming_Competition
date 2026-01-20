ALPHA = 0.75
 
 
class ScapegoatTree:
    def __init__(self, key=0, deleted=True):
        self.left = None
        self.right = None
        self.siz = 0
        self.sm = [0 for _ in range(5)]
        self.key = key
        self.deleted = deleted
        if not self.deleted:
            self.siz += 1
            self.sm[0] += self.key
 
    def add(self, x):
        if x == self.key:
            if self.deleted:
                self.deleted = False
                self.__maintain()
                return True
            else:
                return False
        if x < self.key:
            if self.left is None:
                self.left = ScapegoatTree(key=x, deleted=False)
                self.__maintain()
                return True
            else:
                if self.left.add(x):
                    self.__maintain()
                    if self.left.__unbalanced():
                        self.left = self.__rebuild(self.left)
                    return True
        else:
            if self.right is None:
                self.right = ScapegoatTree(key=x, deleted=False)
                self.__maintain()
                return True
            else:
                if self.right.add(x):
                    self.__maintain()
                    if self.right.__unbalanced():
                        self.right = self.__rebuild(self.right)
                    return True
        return False
 
    def discard(self, x):
        if x == self.key:
            if self.deleted:
                return False
            else:
                self.deleted = True
                self.__maintain()
                return True
        flag = True
        if x < self.key:
            if self.left is None:
                flag = False
            else:
                flag = self.left.discard(x)
        else:
            if self.right is None:
                flag = False
            else:
                flag = self.right.discard(x)
        if flag:
            self.__maintain()
        return flag
 
    def sum(self, i):
        return self.sm[i]
 
    def __maintain(self):
        for i in range(5):
            self.sm[i] = 0
        cnt = 0
        if self.left is not None:
            cnt += self.left.siz
            for i in range(5):
                self.sm[i] += self.left.sm[i]
        if not self.deleted:
            self.sm[cnt % 5] += self.key
            cnt += 1
        if self.right is not None:
            for i in range(5):
                self.sm[(cnt + i) % 5] += self.right.sm[i]
            cnt += self.right.siz
        self.siz = cnt
 
    def __unbalanced(self):
        if self is None or self.siz <= 5:
            return False
        if self.left is not None and self.left.siz > self.siz * ALPHA:
            return True
        if self.right is not None and self.right.siz > self.siz * ALPHA:
            return True
        return False
 
    @classmethod
    def __rebuild(cls, p):
        a = []
 
        def dfs(q):
            if q is None:
                return
            dfs(q.left)
            if not q.deleted:
                a.append(q)
            dfs(q.right)
 
        def build(l, r):
            if l > r:
                return None
            mid = (l + r) // 2
            a[mid].left = build(l, mid - 1)
            a[mid].right = build(mid + 1, r)
            a[mid].__maintain()
            return a[mid]
        dfs(p)
        return build(0, len(a) - 1)