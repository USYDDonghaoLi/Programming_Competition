#lg = {1 << i : i for i in range(32)}

class VebTree:

    __slots__ = {'summary', 'MIN', 'MAX', 'size', 'u', 'divisor'}

    def __init__(self) -> None:
        self.summary = None
        self.MIN = -1
        self.MAX = -1
    
    def build(self, size):
        self.size = size

        if (self.size <= 1):
            self.u = 2
            self.divisor = 1
            return
        
        self.u = 1 << size
        self.divisor = 1 << (size >> 1)
        '''
        cluster_size = ceil(log(u) / 2)
        '''
        cluster_size = (size >> 1) + (size & 1)
        self.cluster = [VebTree() for _ in range(1 << cluster_size)]
        self.summary = VebTree()
        self.summary.build(cluster_size)

        for i in range(1 << cluster_size):
            self.cluster[i].build(size >> 1)
    
    def high(self, x):
        return x // self.divisor
    
    def low(self, x):
        return x % self.divisor

    def index(self, x, y):
        return x * self.divisor + y
    
    def Tree_Minimum(self):
        return self.MIN
    
    def Tree_Maximum(self):
        return self.MAX
    
    def Tree_Member(self, x):
        if (x == self.MIN or x == self.MAX):
            return True
        if self.u == 2:
            return False
        return self.cluster[self.high(x)].Tree_Member(self.low(x))
    
    def Tree_Successor(self, x):
        if self.u == 2:
            if (x == 0 and self.MAX == 1):
                return 1
            return -1
        
        if (self.MIN != -1 and x < self.MIN):
            return self.MIN
        
        MAX_LOW = self.cluster[self.high(x)].Tree_Maximum()
        if (MAX_LOW != -1 and self.low(x) < MAX_LOW):
            offset = self.cluster[self.high(x)].Tree_Successor(self.low(x))
            return self.index(self.high(x), offset)

        succ_cluster = self.summary.Tree_Successor(self.high(x))
        if succ_cluster == -1:
            return -1
        offset = self.cluster[succ_cluster].Tree_Minimum()
        return self.index(succ_cluster, offset)
    
    def Tree_Predecessor(self, x):
        # print('x_info', x, self.high(x), self.low(x))
        # print('nowx=', x, ' MIN= ', self.MIN, ' MAX= ', self.MAX, ' u= ', self.u)
        if self.u == 2:
            if (x == 1 and self.MIN == 0):
                return 0
            return -1
        
        if (self.MAX != -1 and x > self.MAX):
            return self.MAX
        
        MIN_LOW = self.cluster[self.high(x)].Tree_Minimum()
        # print('nowx=', x, ' MIN= ', self.cluster[self.high(x)].MIN, ' MAX= ', self.cluster[self.high(x)].MAX, ' u= ', self.cluster[self.high(x)].u, 'minlow= ', MIN_LOW)
        if (MIN_LOW != -1 and self.low(x) > MIN_LOW):
            offset = self.cluster[self.high(x)].Tree_Predecessor(self.low(x))
            return self.index(self.high(x), offset)

        pred_cluster = self.summary.Tree_Predecessor(self.high(x))
        # print('nowx=', x, ' MIN= ', self.cluster[self.high(x)].MIN, ' MAX= ', self.cluster[self.high(x)].MAX, ' u= ', self.cluster[self.high(x)].u, 'minlow= ', MIN_LOW)
        # print('pred', pred_cluster)
        if pred_cluster == -1:
            if (self.MIN != -1 and x > self.MIN):
                return self.MIN
            return -1
        offset = self.cluster[pred_cluster].Tree_Maximum()
        return self.index(pred_cluster, offset)
    
    def Empty_Tree_Insert(self, x):
        self.MIN = x
        self.MAX = x
    
    def Tree_Insert(self, x):
        if self.MIN == -1:
            self.Empty_Tree_Insert(x)
            return
        
        if x < self.MIN:
            self.MIN, x = x, self.MIN
        
        if self.u > 2:
            if (self.cluster[self.high(x)].Tree_Minimum() == -1):
                self.summary.Tree_Insert(self.high(x))
                self.cluster[self.high(x)].Empty_Tree_Insert(self.low(x))
            else:
                self.cluster[self.high(x)].Tree_Insert(self.low(x))
        
        if x > self.MAX:
            self.MAX = x

    def Tree_Delete(self, x):
        if (self.MIN == self.MAX):
            self.MIN = self.MAX = -1
            return
        
        if self.u == 2:
            if x:
                self.MAX = self.MIN = 0
            else:
                self.MAX = self.MIN = 1
            return
        
        if self.MIN == x:
            first_cluster = self.summary.Tree_Minimum()
            assert first_cluster != -1
            x = self.index(first_cluster, self.cluster[first_cluster].Tree_Minimum())
            self.MIN = x
        
        self.cluster[self.high(x)].Tree_Delete(self.low(x))
        if (self.cluster[self.high(x)].Tree_Minimum() == -1):
            self.summary.Tree_Delete(self.high(x))
            if (x == self.MAX):
                summary_max = self.summary.Tree_Maximum()
                if (summary_max == -1):
                    self.MAX = self.MIN
                else:
                    self.MAX = self.index(summary_max, self.cluster[summary_max].Tree_Maximum())
        elif (x == self.MAX):
            self.MAX = self.index(self.high(x), self.cluster[self.high(x)].Tree_Maximum())