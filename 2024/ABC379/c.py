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

def main():
  n, m = map(int, input().split())
  x_list = list(map(int, input().split()))
  x_list.append(n+1)
  a_list = list(map(int, input().split()))
  a_list.append(1)

  ans = 0
  stone_count = a_list[0]-1
  past_index = 1
  
  if x_list[0] != 1:
    print(-1)
    sys.exit()

  for i in range(1, m+1):
    current_index = x_list[i]
    cell_count = current_index - past_index - 1
    if stone_count < cell_count:
      print(-1)
      sys.exit()
    else:
      ans += (cell_count+1)*cell_count//2
      stone_count -= cell_count
      stone_count += a_list[i]-1
    past_index = current_index
    ic(ans, stone_count)

  if stone_count == 0:
    print(ans)
  else:
    print(-1)


if __name__ == "__main__":
  main()