import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  N, K = map(int, input().split())
  S = input()

  palindrome_list = [False]*(2**K)
  for i in range(2**K):
    flag = True
    for j in range(K // 2):
      if (i >> j & 1) ^ (i >> (K - 1 - j) & 1):
        flag = False
        break

    if flag:
      palindrome_list[i] = True

  # ic(palindrome_list)

  d = {"A": [0], "B": [1], "?": [0, 1]}

  dp_list = [[0]*(2**K) for _ in range(N)]
  for i in range(2**K):
    flag = palindrome_list[i]
    if flag:
      continue
    for j in range(K):
      if not (i >> j & 1) in d[S[j]]:
        flag = True
        break
    if not flag:
      dp_list[K - 1][i] = 1

  # ic(dp_list[K - 1])

  for i in range(K, N):
    c = S[i]
    for x in d[c]:
      for j in range(2**K):
        if palindrome_list[j]:
          continue
        p = j >> 1
        p += x << (K - 1)
        # ic(bin(p))
        if not palindrome_list[p]:
          dp_list[i][p] += dp_list[i - 1][j]

  # print(max(dp_list[-1]) % 998244353)
  print(sum(dp_list[-1]) % 998244353)

if __name__ == "__main__":
  main()