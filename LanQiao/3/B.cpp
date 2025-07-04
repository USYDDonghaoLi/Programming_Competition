#include <bits/stdc++.h>

using namespace std;
int main()
{
  // 请在此输入您的代码
  int n;
  vector<long long> A[n];
  long long res;

  for (int i = 0; i < n; i++) cin >> A[i];

  for (long long a: A){
    long long d = 0;
    if (a >= 500){
      d = max(d, a / 10);
    }

    if (a >= 1000){
      d = max(d, 150LL);
    }

    if (a == 1111){
      d = max(d, 1111LL);
    }

    d = max(d, a / 20);

    res += a - d;
  }

  cout << res << "\n";
  return 0;
}