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
  n, c = map(int, input().split())
  t_list = list(map(int, input().split()))

  ans = 0
  prev = -(10**9)

  for t in t_list:
    if c <= t - prev:
      ans += 1
      prev = t
    ic(t, prev, ans)

  print(ans)

if __name__ == "__main__":
  main()