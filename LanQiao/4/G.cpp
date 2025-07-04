#include<bits/stdc++.h>
using namespace std;
namespace mcmf
{
	const int MAXN=23333,MAXM=233333;
	struct edge
	{
		int v,f,w;
		edge *next,*rev;
	}*h[MAXN],pool[MAXM*2];
	int top;
	inline void addedge(int u,int v,int c,int w)
	{
		cout<<u<<' '<<v<<' '<<c<<' '<<w<<endl;
		edge *tmp=&pool[top++];tmp->v=v;tmp->f=c;tmp->w=w;tmp->next=h[u];h[u]=tmp;
		edge *pmt=&pool[top++];pmt->v=u;pmt->f=0;pmt->w=-w;pmt->next=h[v];h[v]=pmt;
		tmp->rev=pmt;pmt->rev=tmp;
	}
	deque<int> q;
	int S,T;
	int last[MAXN],inq[MAXN];
	long long dis[MAXN],maxf[MAXN];
	edge *laste[MAXN];
	long long totcost,totflow;
	bool SPFA()
	{
		memset(dis,0x3f,sizeof(dis));
		memset(last,0,sizeof(last));
		memset(maxf,0,sizeof(maxf));
		memset(inq,0,sizeof(inq));
		while(!q.empty())q.pop_front();
		q.push_front(S);
		maxf[S]=0x3f3f3f3f3f3f3f3fll;
		inq[S]=1;
		dis[S]=0;
		while(!q.empty())
		{
			int u=q.front();q.pop_front();
			inq[u]=0;
			for(edge *tmp=h[u];tmp;tmp=tmp->next)
			{
				if(tmp->f&&dis[tmp->v]>dis[u]+tmp->w)
				{
					dis[tmp->v]=dis[u]+tmp->w;
					last[tmp->v]=u;
					maxf[tmp->v]=min(maxf[u],(long long)tmp->f);
					laste[tmp->v]=tmp;
					if(!inq[tmp->v])
					{
						if(q.empty()||dis[q.front()]>dis[tmp->v])
							q.push_front(tmp->v);
						else q.push_back(tmp->v);
						inq[tmp->v]=1;
					}
				}
			}
		}
		if(dis[T]>=0x3f3f3f3f3f3f3f3fll)return false;
		int u=T;
		maxf[T]=1;
		while(last[u])
		{
			laste[u]->f-=maxf[T];
			laste[u]->rev->f+=maxf[T];
			u=last[u];
		}
		totcost+=dis[T]*maxf[T];
		totflow+=maxf[T];
		return true;
	}
}
int main()
{
	ios_base::sync_with_stdio(false);
	int n;
	cin>>n;
	vector<int> a(n+5);
	vector<int> pre(11);
	map<int,int> pre11;
	for(int i=1;i<=n;i++)
	{
		cin>>a[i];
	}
	mcmf::S=n*2+1;mcmf::T=n*2+2;
	for(int i=1;i<=n;i++)
	{
		mcmf::addedge(mcmf::S,i,1,0);
		mcmf::addedge(i+n,mcmf::T,1,0);
		mcmf::addedge(i,i+n,1,-1);
		if(pre[a[i]%9])
		{
			mcmf::addedge(pre[a[i]%9],i,10000,0);
			mcmf::addedge(pre[a[i]%9]+n,i,10000,0);
		}
		if(pre11.count(a[i]-11))
		{
			mcmf::addedge(pre11[a[i]-11],i,10000,0);
			mcmf::addedge(pre11[a[i]-11]+n,i,10000,0);
		}
		if(pre11.count(a[i]+11))
		{
			mcmf::addedge(pre11[a[i]+11],i,10000,0);
			mcmf::addedge(pre11[a[i]+11]+n,i,10000,0);
		}
		pre[a[i]%9]=i;
		pre11[a[i]]=i;
	}
	mcmf::addedge(n+1,mcmf::T,1,0);
	for(int i=1;i<=min(n,9);i++)
	{
		mcmf::SPFA();
		cout<<-mcmf::totcost<<" \n"[i==n];
	}
	for(int i=10;i<=n;i++)
	{
		cout<<-mcmf::totcost<<" \n"[i==n];
	}
	return 0;
}