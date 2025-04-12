// Original Python code:
// 
// def main():
//   n, k = map(int, input().split())
// 
//   a_list = [0]*(n+1)
// 
//   shakutori = 0
// 
//   for i in range(n+1):
//     if i < k:
//       a_list[i] = 1
//       shakutori += 1
//     else:
//       a = shakutori
//       a_list[i] = a
//       shakutori -= a_list[i - k]
//       shakutori += a
// 
//   print(a_list[n]%10**9)
// 
// if __name__ == "__main__":
//   main()

#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n, k;
    cin >> n >> k;

    vector<long long> a_list(n + 1, 0);
    long long shakutori = 0;
    const long long MOD = 1000000000LL;

    for (long long i = 0; i <= n; i++) {
        if (i < k) {
            a_list[i] = 1;
            shakutori += 1;
        } else {
            long long a = shakutori;
            a_list[i] = a;
            shakutori -= a_list[i - k];
            shakutori += a;
        }
    }

    cout << (a_list[n] % MOD) << "\n";
    return 0;
}
