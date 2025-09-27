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
  N = int(input())
  a_list = list(map(int, input().split()))

  num_count_list = [0] * (N + 2)

  for a in a_list:
    num_count_list[a] += 1

  num_count_list[-1] = 0

  is_valid = not any([count > 1 for count in num_count_list])

  ic(num_count_list)

  if is_valid:
    print("Yes")
  else:
    print("No")
    sys.exit()

  num_pool = set(range(1, N + 1))

  for i in range(N):
    if a_list[i] != -1:
      num_pool.discard(a_list[i])

  num_queue = list(num_pool)

  ans_list = a_list[:]

  for i in range(N):
    if ans_list[i] == -1:
      x = num_queue.pop()
      ans_list[i] = x

  print(*ans_list)

if __name__ == "__main__":
  main()