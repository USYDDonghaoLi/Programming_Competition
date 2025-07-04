#include <bits/stdc++.h>
using namespace std;
using i64 = int64_t;
struct Event {
  int x, y, sign, id;
  bool operator<(const Event& rhs) const {
    return pair<int, int>(x, id) < pair<int, int>(rhs.x, rhs.id);
  }
};
int main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int n, q;
  int m = 200000;
  cin >> n >> q;
  vector<Event> events;
  for (int i = 0, l, r; i < n; i += 1) {
    cin >> l >> r;
    events.push_back({l, r, 0, -1});
  }
  vector<int> ans(q);
  for (int i = 0, a, b; i < q; i += 1) {
    cin >> a >> b;
    if (a < b) {
      int x0 = 1, x1 = a;
      int y0 = a, y1 = b - 1;
      events.push_back({x1, y1, 1, i});
      events.push_back({x0 - 1, y1, -1, i});
      events.push_back({x1, y0 - 1, -1, i});
      events.push_back({x0 - 1, y0 - 1, 1, i});
    }
    if (a > b) {
      int x0 = b + 1, x1 = a;
      int y0 = a, y1 = m;
      events.push_back({x1, y1, 1, i});
      events.push_back({x0 - 1, y1, -1, i});
      events.push_back({x1, y0 - 1, -1, i});
      events.push_back({x0 - 1, y0 - 1, 1, i});
    }
  }
  vector<int> bit(m + 1);
  auto add = [&](int x) {
    for (; x <= m; x += x & -x) { bit[x] += 1; }
  };
  auto sum = [&](int x) {
    int y = 0;
    for (; x; x -= x & -x) { y += bit[x]; }
    return y;
  };
  sort(events.begin(), events.end());
  for (auto e : events) {
    int x = e.x;
    int y = e.y;
    int id = e.id;
    int sign = e.sign;
    if (id == -1) {
      add(y);
    } else {
      ans[id] += sum(y) * sign;
    }
    cout << " " << x << y << id << sign << "\n";
  }
  for (int x : ans) { cout << x << "\n"; }
}