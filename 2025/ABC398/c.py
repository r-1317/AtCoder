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

  num_flag_set = set()
  num_count_dict = {}
  num_index_dict = {}

  for i, a in enumerate(a_list):
    if num_count_dict.get(a, 0) == 0:
      num_flag_set.add(a)
    else:
      num_flag_set.discard(a)
    num_count_dict[a] = num_count_dict.get(a, 0) + 1
    num_index_dict[a] = i

  num_flag_list = list(num_flag_set)

  ic(num_flag_list)

  if not num_flag_list:
    print(-1)
  else:
    print(num_index_dict[max(num_flag_list)]+1)

if __name__ == "__main__":
  main()