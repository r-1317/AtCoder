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
  n, m = map(int, input().split())
  a_list = list(map(int, input().split()))
  b_list = list(map(int, input().split()))

  a_list.sort()
  b_list.sort()

  ic(a_list)
  ic(b_list)

  ans = 0
  tmp = 0

  for i in range(n):
    if b_list[tmp] <= a_list[i]:
      tmp += 1
      ans += a_list[i]
      if tmp == m:
        break

  if tmp == m:
    print(ans)
  else:
    print(-1)

if __name__ == "__main__":
  main()