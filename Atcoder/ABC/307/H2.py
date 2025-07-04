import numpy as np

def c2n(c):
  if c=='_': return 0
  return ord(c)

N,W=map(int,input().split())
T=input()
P=input()
T=T+("."*(W-1))+T
if W==N:
  T=T[:-1]
else:
  T=T+("."*(W-N-1))

T1=np.array(list(map(c2n,T)))
P1=np.array(list(map(c2n,P[::-1])))

#T1.resize(len(T)*2)
P1.resize(T1.shape)
T2=T1*T1
P2=P1*P1
P3=sum(P2*P1)

X1=np.fft.ifft(np.fft.fft(T2)*np.fft.fft(P1))
X2=np.fft.ifft(np.fft.fft(T1)*np.fft.fft(P2))

print(sum(1 for i in range(W-1,(W-1)+(N+W-1)) if abs(X1[i]-2*X2[i]+P3)<10**-2))