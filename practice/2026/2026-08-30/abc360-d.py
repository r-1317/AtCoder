import os
import bisect

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  N, T = map(int, input().split())
  S = input()
  x_list = list(map(int, input().split()))

  east_list = []
  west_list = []
  for i in range(N):
    c = S[i]
    if c == "1":
      east_list.append(x_list[i])
    else:
      west_list.append(x_list[i])

  east_list.sort()  # このソートは要らないかも
  west_list.sort()

  ans = 0
  for e in east_list:
    l = bisect.bisect_left(west_list, e)
    r = bisect.bisect_right(west_list, e + 2*T)
    ans += r - l

  print(ans)


if __name__ == "__main__":
  main()