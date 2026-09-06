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
  N = int(input())
  a_list = list(map(int, input().split()))
  b_list = list(map(int, input().split()))

  for i in range(N):
    min_num = min(a_list[i], b_list[i])
    a_list[i] -= min_num
    b_list[i] -= min_num

  takahashi_count = 0
  aoki_count = 0

  w_list = [1]*N
  for i in range(N):
    if a_list[i] > 0:
      w_list[i] = 10**18
      takahashi_count += a_list[i]
    else:
      aoki_count += b_list[i]

  if takahashi_count * 10**18 > aoki_count:
    print("Yes")
    print(*w_list)
  else:
    print("No")


if __name__ == "__main__":
  main()