n=input()
s=list(map(int,input().split()))
suyinzilist=[]
path=[]
tmp=[]  
def sushu(k):
    for i in range(2,int(k*0.5)+1):
        if k%i==0:
            return False
    return True
def suyinzi(m):
    yzlist=[]
    for i in range(2,m+1):
        while m%i==0:
            if i not in yzlist and sushu(i):
                yzlist.append(i)
            m=m//i
    return yzlist
def sou(suyinzilist,tmp):
    if not suyinzilist:
        path.append(tmp)
        return True
    else:
        for i in suyinzilist[0]:
            if i not in tmp:
                sou(suyinzilist[1:],tmp+[i])

for i in s:
    suyinzilist.append(suyinzi(i))
    
sou(suyinzilist,tmp) 

if len(path)==0:
    print('-1')
    exit()    
minsum=sum(path[0])
for i in path:
    minsum=min(minsum,sum(i))
print(minsum)