#include<bits/stdc++.h>

void ask(std::vector<int> idxs) {
    std::cout << "- " << idxs.size();
    for(int i = 0; i < idxs.size(); i++) {
        std::cout << " " << idxs[i];
    }
    std::cout << std::endl;
}

void answer(int idx) {
    std::cout << "! " << idx << std::endl;
}

void solve(int testcase) {
    int n;
    std::cin >> n;
    std::vector<int> nums(n);
    for(int i = 0; i < n; i++) {
        std::cin >> nums[i];
    }
    std::map<int, int> mp; // Equivalent to Counter in Python
    for(int num : nums) {
        mp[num]++;
    }
    ask(std::vector<int>());
    std::vector<int> newNums(n);
    for(int i = 0; i < n; i++) {
        std::cin >> newNums[i];
    }
    if(newNums.size() == 1) {
        answer(1);
        return;
    }
    std::map<int, int> newMp; // Equivalent to Counter in Python
    for(int num : newNums) {
        newMp[num]++;
    }
    int name = -1;
    for(auto it = newMp.begin(); it != newMp.end(); ++it) {
        if(it->second > mp[it->first]) {
            name = it->first;
            break;
        }
    }
    assert(name != -1);
    mp.clear();
    mp[name] = newMp[name];
    std::vector<int> idxs;
    for(int i = 0; i < newNums.size(); i++) {
        if(newNums[i] != name) {
            idxs.push_back(i + 1);
        }
    }
    ask(idxs);
    // You would need to handle input again here
    // Repeat similar blocks as needed
}

int main(){
    std::ios_base::sync_with_stdio(0); std::in.tie(0); std::cout.tie(0);
    int T = 1;
    cin >> T;
    for (int testcase = 1; testcase <= T; testcase++) solve(testcase);
    return 0;
}