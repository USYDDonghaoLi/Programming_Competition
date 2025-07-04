#include<bits/stdc++.h>
using namespace std;
int a[200010],dp1[200010],dp2[200010];

int main()
{
    int n;
    cin>>n;
    
    for(int i=1;i<=n;i++)
    {
        cin>>a[i];
        dp1[i]=dp2[i]=1;//初始化
    }
    
    for(int i=1;i<=n;i++)
        for(int j=1;j<i;j++)
            if(a[i]>a[j])dp1[i]=max(dp1[i],dp1[j]+1);
    
    for(int i=n;i>=1;i--)
        for(int j=n;j>i;j--)
            if(a[i]<a[j])dp2[i]=max(dp2[i],dp2[j]+1);
    
    int ans=0;
    for(int i=0;i<=n;i++)
        for(int j=i+2;j<=n+1;j++)
        {
            if(a[i]+2<=a[j])ans=max(ans,dp1[i]+dp2[j]+1);//左边+修改值(长度为1)+右边
            if(a[j]>0)ans=max(ans,dp2[j]+1);//因为最小只能改为0,a[j]>0才能将修改值与右边拼接
            ans=max(ans,dp1[i]+1);//因为可以改无穷大,所以一定可以将修改值与左边拼接
        }
    cout<<ans;
    
    return 0;
}