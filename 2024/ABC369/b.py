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
  n = int(input())
  l_list = []
  r_list = []

  for i in range(n):
    a, s = map(str, input().split())
    a = int(a)

    if s == "R":
      r_list.append(a)
    else:
      l_list.append(a)

  ic(l_list)
  ic(r_list)

  ans = 0

  for i, l in enumerate(l_list):
    if i == 0:
      continue

    ans += abs(l - l_list[i - 1])

  for i, r in enumerate(r_list):
    if i == 0:
      continue

    ans += abs(r - r_list[i - 1])

  print(ans)

if __name__ == "__main__":
  main()