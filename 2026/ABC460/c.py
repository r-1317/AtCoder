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
  a_list = list(map(int, input().split()))
  b_list = list(map(int, input().split()))
  a_list.sort(reverse=True)
  b_list.sort(reverse=True)

  ans = 0
  b_idx = 0
  flag = False

  for a in a_list:
    while a*2 < b_list[b_idx]:
      b_idx += 1
      if b_idx >= M:
        flag = True
        break
    if flag:
      break
    ans += 1
    b_idx += 1
    if b_idx >= M:
      flag = True
      break

  print(ans)


if __name__ == "__main__":
  main()