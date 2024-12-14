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

def prev_main():
  n, s = map(int, input().split())
  a_list = list(map(int, input().split()))
  cum_sum = [0] * (n+1)
  for i in range(n):
    cum_sum[i+1] = cum_sum[i] + a_list[i]

  reversed_cum_sum = [0] * (n+1)
  reversed_cum_sum[n-1] = a_list[n-1]
  for i in range(n-2, -1, -1):
    reversed_cum_sum[i] = reversed_cum_sum[i+1] + a_list[i]

  reversed_cum_sum.reverse()

  ic(cum_sum)
  ic(reversed_cum_sum)

  ic(len(cum_sum), len(reversed_cum_sum))

  ic(s)
  ic(s // cum_sum[-1])
  s %= cum_sum[-1]
  ic(s)

  flag = False

  for x in cum_sum:
    y = reversed_cum_sum[bisect.bisect_left(reversed_cum_sum, s-x)]
    # ic(x, s-x, y)
    if x + y == s:
      flag = True
      break

    if MyPC:
      for y in reversed_cum_sum:
        # ic(x, s-x, y)
        if x + y == s:
          flag = True
          break

  print("Yes" if flag else "No")

def main():
  n, s = map(int, input().split())
  a_list = list(map(int, input().split()))
  cum_sum = [0] * (n*2)
  cum_sum[0] = a_list[0]
  for i in range(1, n*2):
    cum_sum[i] = cum_sum[i-1] + a_list[i%n]
  
  s %= cum_sum[n-1]
  ic(s)
  ic(cum_sum)

  flag = False
  for i in range(n):
    x = cum_sum[i]
    y = cum_sum[bisect.bisect_left(cum_sum, s+x)]
    if y - x == s:
      flag = True
      break

  print("Yes" if flag else "No")


if __name__ == "__main__":
  main()