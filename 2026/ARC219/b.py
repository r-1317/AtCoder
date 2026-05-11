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
  T = int(input())

  for _ in range(T):
    N = int(input())
    p_list = list(map(int, input().split()))
    ans = 0
    if p_list == list(range(1, N+1)):
      ans = 1
    for i, p in enumerate(p_list):
      if p == i+1:
        ans += N - i - 1
      else:
        break
    ans %= 998244353
    ic(ans)
    print(ans)

if __name__ == "__main__":
  main()