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

  num_count_list = [0]*(n+1)
  num_count = 0

  for i, a in enumerate(a_list):
    if not num_count_list[a]:
      num_count += 1
    num_count_list[a] += 1

  new_num_count_list = [0]*(n+1)
  new_num_count = 0

  max_num_count_sum = 0

  ic(num_count, new_num_count)

  for i, a in enumerate(a_list):
    num_count_list[a] -= 1
    if not num_count_list[a]:
      num_count -= 1
    if not new_num_count_list[a]:
      new_num_count += 1
    new_num_count_list[a] += 1
    max_num_count_sum = max(max_num_count_sum, num_count+new_num_count)

  print(max_num_count_sum)

if __name__ == "__main__":
  main()