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
  N, M = map(int, input().split())

  ans = 0

  for i in range(61):
    if not(M >> i & 1):
      continue
    cycle_len = 2**(i+1)
    cycle_count = N // cycle_len
    rem = N - cycle_len * cycle_count
    rem = max(0, rem - cycle_len // 2 + 1)
    ans += cycle_count * cycle_len // 2 + rem

    ans %= 998244353

  print(ans % 998244353)

if __name__ == "__main__":
  main()