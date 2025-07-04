#include <bits/stdc++.h>
using namespace std;

int ask(int l, int r){
    int ret;
    printf("? %d %d\n", l, r);
    fflush(stdout);
    scanf("%d", &ret);
    return ret;
}

void answer(int ans){
    printf("! %d\n", ans);
    fflush(stdout);
    return;
}

int n, res, res1, res2;
int arr[1 << 18];

void solve(){
    scanf("%d", &n);
    memset(arr, 0, sizeof(arr));

    for (int i = 1; i <= (1 << n); ++i) arr[i] = i;
    int idxl = 1, idxr = (1 << n) + 1;
    while (true){
        int a = arr[idxl], b = arr[idxl + 1], c = arr[idxl + 2], d = arr[idxl + 3];

        if (b == 0){
            answer(a);
            return;
        }
        else if (c == 0){
            res = ask(a, b);
            if (res == 1){
                answer(a);
                return;
            }
            else{
                answer(b);
                return;
            }
        }
        else{
            res1 = ask(a, d);
            if (res1 == 1){
                res2 = ask(a, c);
                if (res2 == 1){
                    arr[idxr] = a;
                }
                else{
                    arr[idxr] = c;
                }
            }
            else if (res1 == 0){
                res2 = ask(b, c);
                if (res2 == 1){
                    arr[idxr] = b;
                }
                else{
                    arr[idxr] = c;
                }
            }
            else{
                res2 = ask(b, d);
                if (res2 == 1){
                    arr[idxr] = b;
                }
                else{
                    arr[idxr] = d;
                }
            }
        idxr++;
        idxl += 4; 
        }
    }
}

int main(){
    int T;
    scanf("%d", &T);
    for (;T--;) solve();
}