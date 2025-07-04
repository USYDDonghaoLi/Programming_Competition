from sys import stdin
input=lambda :stdin.readline()[:-1]

class segtree():
    n=1
    size=1
    log=2
    d=[0]
    op=None
    e=10**15
    def __init__(self,V,OP,E):
        self.n=len(V)
        self.op=OP
        self.e=E
        self.log=(self.n-1).bit_length()
        self.size=1<<self.log
        self.d=[E for i in range(2*self.size)]
        for i in range(self.n):
            self.d[self.size+i]=V[i]
        for i in range(self.size-1,0,-1):
            self.update(i)
    def set(self,p,x):
        assert 0<=p and p<self.n
        p+=self.size
        self.d[p]=x
        for i in range(1,self.log+1):
            self.update(p>>i)
    def get(self,p):
        assert 0<=p and p<self.n
        return self.d[p+self.size]
    def prod(self,l,r):
        assert 0<=l and l<=r and r<=self.n
        sml=self.e
        smr=self.e
        l+=self.size
        r+=self.size
        while(l<r):
            if (l&1):
                sml=self.op(sml,self.d[l])
                l+=1
            if (r&1):
                smr=self.op(self.d[r-1],smr)
                r-=1
            l>>=1
            r>>=1
        return self.op(sml,smr)
    def all_prod(self):
        return self.d[1]
    def max_right(self,l,f):
        assert 0<=l and l<=self.n
        assert f(self.e)
        if l==self.n:
            return self.n
        l+=self.size
        sm=self.e
        while(1):
            while(l%2==0):
                l>>=1
            if not(f(self.op(sm,self.d[l]))):
                while(l<self.size):
                    l=2*l
                    if f(self.op(sm,self.d[l])):
                        sm=self.op(sm,self.d[l])
                        l+=1
                return l-self.size
            sm=self.op(sm,self.d[l])
            l+=1
            if (l&-l)==l:
                break
        return self.n
    def min_left(self,r,f):
        assert 0<=r and r<self.n
        assert f(self.e)
        if r==0:
            return 0
        r+=self.size
        sm=self.e
        while(1):
            r-=1
            while(r>1 & (r%2)):
                r>>=1
            if not(f(self.op(self.d[r],sm))):
                while(r<self.size):
                    r=(2*r+1)
                    if f(self.op(self.d[r],sm)):
                        sm=self.op(self.d[r],sm)
                        r-=1
                return r+1-self.size
            sm=self.op(self.d[r],sm)
            if (r& -r)==r:
                break
        return 0
    def update(self,k):
        self.d[k]=self.op(self.d[2*k],self.d[2*k+1])
    def __str__(self):
        return str([self.get(i) for i in range(self.n)])

n=int(input())
a=[0]*n
b=[0]*n
for i in range(n):
  a[i],b[i]=map(int,input().split())
s=set(a)
q=int(input())
query=[]
for _ in range(q):
  t,*xy=map(int,input().split())
  if t==1:
    query.append((t,xy[0],xy[1]))
    s.add(xy[1])
  if t==2:
    query.append((t,xy[0],xy[1]))
  if t==3:
    query.append((t,xy[0],-1))

s=sorted(list(s),reverse=True)
m=len(s)
d={}
for i in range(m):
  d[s[i]]=i

c1=[0]*m
c2=[0]*m
for i in range(n):
  c1[d[a[i]]]+=b[i]
  c2[d[a[i]]]+=a[i]*b[i]

seg1=segtree(c1,lambda x,y:x+y,0)
seg2=segtree(c2,lambda x,y:x+y,0)

ans=[]
#print(a,b)
for t,x,y in query:
  if t==1:
    x-=1
    dx=d[a[x]]
    
    seg1.set(dx,seg1.get(dx)-b[x])
    seg2.set(dx,seg2.get(dx)-a[x]*b[x])
    
    a[x]=y
    dx=d[a[x]]
    
    seg1.set(dx,seg1.get(dx)+b[x])
    seg2.set(dx,seg2.get(dx)+a[x]*b[x])
  if t==2:
    x-=1
    dx=d[a[x]]

    seg1.set(dx,seg1.get(dx)-b[x])
    seg2.set(dx,seg2.get(dx)-a[x]*b[x])
    
    b[x]=y
    dx=d[a[x]]
    
    seg1.set(dx,seg1.get(dx)+b[x])
    seg2.set(dx,seg2.get(dx)+a[x]*b[x])
  if t==3:
    def f(T):
      return T<x
    R=seg1.max_right(0,f)
    # print('R',R)
    if R==m:
      print(-1)
      continue
    c=seg1.prod(0,R)
    res=seg2.prod(0,R)
    # print('xcres', x, c, res)
    print(res+s[R]*(x-c))
#   print(seg1.d)
#   print(seg2.d)