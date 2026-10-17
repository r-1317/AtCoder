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
  N, K, T = map(int, input().split())
  a_list = list(map(int, input().split())) + [T]  # 最後のは実装の都合で足した
  a_list.sort()

  for i, a in enumerate(a_list):
    if a > T:
      a_list = a_list[:i]
      break

  ic(a_list)

  ans = 0
  stop_time = 0
  for a in a_list:
    if a <= stop_time:
      ic(a)
      stop_time = a + K
    else:
      diff = a - stop_time
      ic(stop_time, diff)
      ans += (diff + K - 1) // K
      stop_time = a + K

  print(ans)

if __name__ == "__main__":
  main()