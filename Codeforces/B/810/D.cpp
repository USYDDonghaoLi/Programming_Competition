#include <bits/stdc++.h>
#define MAXN 200100
#define LL long long
using namespace std;

typedef pair<LL,LL> pll;
LL n,m;
LL x[MAXN],p[MAXN];
vector<pll> diff;
pll key;

pll getIntersection(pll p1,pll p2)
{
	LL tx=max(p1.first+p1.second,p2.first+p2.second);
	LL ty=max(p1.second-p1.first,p2.second-p2.first);
	return {(tx-ty)/2,(tx+ty)/2};
}

void work()
{
	diff.clear();
	key={0,-0x3f3f3f3f3f3f3f3f};
	cin>>n>>m;
	m*=2;
	for (int i=1;i<=n;i++)
	{
		cin>>x[i]>>p[i];
		x[i]*=2;
		p[i]*=2;
		diff.push_back({x[i]-p[i],1});
		diff.push_back({x[i],-2});
		diff.push_back({x[i]+p[i],1});
	}
	sort(diff.begin(), diff.end());

	LL a=0,d=0;
	LL lst=0;
	for (auto p:diff)
	{
        //cout << p.first << ' ' << p.second << endl;
		if (p.first!=lst)
		{
			a=a+(p.first-lst)*d;
			lst=p.first;
			if (a>m)
				key=getIntersection(key,{p.first,a-m});
		}
		d+=p.second;
        cout << a << ' ' << d << endl;
        //printf("testad %lld %lld\n", a, d);
        //printf("test %lld %lld\n", key.first, key.second);
	}
    //printf("test %lld %lld\n", key.first, key.second);
	for (int i=1;i<=n;i++)
		if (getIntersection(key,{x[i],p[i]})==pll(x[i],p[i]))
			cout<<'1';
		else
			cout<<'0';
	cout<<endl;
}

int main()
{
	int casenum=1;
	cin>>casenum;
	for (int testcase=1;testcase<=casenum;testcase++)
		work();
	return 0;
}