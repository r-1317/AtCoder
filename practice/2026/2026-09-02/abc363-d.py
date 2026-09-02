import os
import sys

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def rec(N, k, count, l, i):
  if i >= (k+1)//2:
    return l

  for j in range(11):
    if i == 0 and j == 0:
      continue

    if count + 10**((k+1)//2 - 1 - i) >= N:
      break

    count += 10**((k+1)//2 - 1 - i)

  return rec(N, k, count, l + str(j), i+1)

def main():
  N = int(input())

  if N == 1:  # 実装上こうしたほうが楽だと思う
    print(0)
    sys.exit()

  count = 1
  for k in range(1, 10**9):
    if count + (9 * 10**((k+1)//2 - 1)) > N:
      break
    count += 9 * 10**((k+1)//2 - 1)

  l = rec(N, k, count, "", 0)
  ic(k, l)
  r = l[::-1]
  if k % 2:
    r = r[1:]

  ans = l + r
  print(ans)

if __name__ == "__main__":
  main()