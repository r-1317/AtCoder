#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll MOD = 998244353;


int main(){
  int N;
  cin >> N;

  // 文字列の集合
  set<string> S;

  // 文字列の配列
  vector<string> A(N);
  for (int i = 0; i < N; i++) {
    cin >> A[i];
  }
  
  for (int i = 0; i < N; i++) {
    for (int j = i+1; j < N; j++){
      string t = A[i] + A[j];
      if (S.find(t) == S.end()) {
        S.insert(t);
      }
    }
  }

  // Sの要素数
  cout << S.size() << endl;
}
