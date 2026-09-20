import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

MOD = 998244353

def main():
  N = int(input())
  # print(int(str(N)*N)%998244353)

  k = len(str(N))
  r = 10**k % MOD

  ans = N * (pow(r, N, MOD) - 1) * pow(r - 1, -1, MOD)

  print(ans % MOD)

if __name__ == "__main__":
  main()