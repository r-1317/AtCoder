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
  n = int(input())
  a_list = list(map(int, input().split()))

  ans = 0

  num_index_list = [-1] * (n+1)

  tmp_start = 0
  tmp = -1
  tmp_count = 1
  last_pair_index = -1

  

  for i, a in enumerate(a_list):
    if a == tmp:
      tmp_count += 1
      if tmp_count == 2:
        if num_index_list[a] < tmp_start:
          num_index_list[a] = i
        else:
          ans = max(ans, last_pair_index - tmp_start + 1)
          tmp_start = num_index_list[a]+1
      else:
        ans = max(ans, last_pair_index - tmp_start + 1)
        tmp_start = i-1
        last_pair_index = i
        num_index_list[a] = i
      last_pair_index = i
    
    else:
      if last_pair_index == i-1:
        tmp_count = 1
      else:
        ans = max(ans, last_pair_index - tmp_start + 1)
        tmp_count = 1
        tmp_start = i
        last_pair_index = i-1

    tmp = a

    ic(i, a, tmp, tmp_count, tmp_start, last_pair_index, ans)

  print(max(ans, last_pair_index - tmp_start + 1))


if __name__ == "__main__":
  main()

  # for i, a in enumerate(a_list):
  #   if tmp_count == 1:
  #     if a == tmp:
  #       tmp_count += 1
  #       if num_index_list[a] < tmp_start:
  #         num_index_list[a] = i
  #       else:
  #         ans = max(ans, last_pair_index - tmp_start + 1)
  #         tmp_start = num_index_list[a]+1
  #       last_pair_index = i
  #     else:
  #       ans = max(ans, last_pair_index - tmp_start + 1)
  #       tmp = a
  #       tmp_count = 1
  #       tmp_start = i
  #       last_pair_index = i-1

  #   else:
  #     if a == tmp:
  #       ans = max(ans, last_pair_index - tmp_start + 1)
  #       tmp_count += 1
  #       tmp_start = i-1
  #       last_pair_index = i
  #     else:
  #       tmp = a
  #       tmp_count = 1
  #       tmp_start = i
  #       last_pair_index = i
  
  #   ic(i, a, tmp, tmp_count, tmp_start, last_pair_index, ans)