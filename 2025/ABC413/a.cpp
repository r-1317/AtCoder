#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll MOD = 998244353;


int main(){
  int N, M;
  cin >> N >> M;
  vector<int> A(N);
  for (int i = 0; i < N; i++) {
    cin >> A[i];
  }

  int sum = 0;
  cerr << sum << endl;

  cerr << "N: " << N << ", M: " << M << endl;

  for (int i = 0; i < N; i++) {
    sum += A[i];
    cerr << "A[" << i << "] = " << A[i] << ", Current sum: " << sum << endl;
  }

  cerr << "Sum of elements: " << sum << endl;

  if (sum <= M) cout << "Yes" << endl;
  else cout << "No" << endl;
  return 0;
}
