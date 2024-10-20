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
  a_list = list(map(int, input().split()))
  b_list = list(map(int, input().split()))
  a_list.sort(reverse=True)
  b_list.sort(reverse=True)
  b_list.append(0)

  ans = 0
  flag = False
  count = 0
  x = 0

  for i in range(n):
    if a_list[i] <= b_list[count]:
      count += 1
    else:
      if x:  # すでにxがある場合
        flag = True
        break
      x = a_list[i]

  if flag:
    print(-1)
  else:
    print(x)


if __name__ == "__main__":
  main()