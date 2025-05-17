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
  p_list = list(map(int, input().split()))
  p_list.append(-1)  # 最後に強制的にupでなくする

  up_count_list = [0] * (n + 1)
  up_count_index = 0
  is_up = False
  ans = 0

  for i in range(n):
    if p_list[i] < p_list[i + 1]:
      if not is_up:
        is_up = True
      up_count_list[up_count_index] += 1
    else:
      if is_up:
        is_up = False
        # up_count_index += 1
        if up_count_index != 0:
          ans += up_count_list[up_count_index] * up_count_list[up_count_index-1]
        up_count_index += 1
    ic(up_count_index, up_count_list)

  print(ans)

if __name__ == "__main__":
  main()