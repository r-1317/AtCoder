import os
import math

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
  rigai_count_list = [N-1]*N

  for _ in range(M):
    a, b = map(int, input().split())
    a -= 1
    b -= 1
    rigai_count_list[a] -= 1
    rigai_count_list[b] -= 1

  # kaijyou_list = [0]*N
  # kaijyou_list[0] = 1
  # for i in range(1, N):
  #   kaijyou_list[i] = kaijyou_list[i-1] * i

  ans_list = [-1]*N

  for i in range(N):
    if rigai_count_list[i] < 3:
      ans_list[i] = 0
    else:
      ans_list[i] = rigai_count_list[i] * (rigai_count_list[i] - 1) * (rigai_count_list[i] - 2) // 6

  print(*ans_list)

if __name__ == "__main__":
  main()