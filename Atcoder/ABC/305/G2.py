def naive(n,m,s):
  ans=0
  for bit in range(1<<n):
    res=''
    for i in range(n):
      if (bit>>i)&1:
        res+='a'
      else:
        res+='b'
    flag=True
    for i in s:
      if i in res:
        flag=False
    if flag:
      ans+=1
  return ans

mod=998244353

def matmul(A,B):
    res = [[0]*len(B[0]) for _ in [None]*len(A)]
    for i, resi in enumerate(res):
        for k, aik in enumerate(A[i]):
            for j,bkj in enumerate(B[k]):
                resi[j] += aik*bkj
                resi[j] %= mod
    return res

def matpow(A,p):
    if p%2:
        return matmul(A, matpow(A,p-1))
    elif p > 0:
        b = matpow(A,p//2)
        return matmul(b,b)
    else:
        return [[int(i==j) for j in range(len(A))] for i in range(len(A))]


def solve(n,m,s):
  A=[[0]*64 for i in range(64)]
  B=[[0] for i in range(64)]
  cnt=[0]*64
  for bit in range(1<<6):
    res=''
    for i in range(6):
      if (bit>>i)&1:
        res+='a'
      else:
        res+='b'
    
    flag1=True
    for j in s:
      if j in res:
        flag1=False
    if not flag1:
      continue
    for i in range(2):
      nbit=(bit)//2+(32*i)
      if i==0:
        nres=res[1:]+'b'
      else:
        nres=res[1:]+'a'
      flag=True
      for j in s:
        if j in nres:
          flag=False
      cnt[nbit]+=1
      if flag:
        A[bit][nbit]=1
        B[nbit][0]=1
#   for i in range(64):
#     for j in range(64):
#       if A[i][j]:
#         print(i, j, A[i][j])
#   for i in range(64):
#     if B[i][0]:
#       print(i, B[i][0])
  
  C=matpow(A,n-6)
  for i in range(64):
     for j in range(64):
        if C[i][j]:
           print(i, j, C[i][j])
  D=matmul(C,B)
  ans=0
  for i in range(64):
    ans+=D[i][0]
    if D[i][0]:
      print(i, D[i][0])
  return ans%mod

n,m=map(int,input().split())
s=[input() for i in range(m)]
print(solve(n,m,s)%mod)