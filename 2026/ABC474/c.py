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
  N, Q = map(int, input().split())
  p_list = list(map(int, input().split()))

  idx_list = [-1]*(N+1)
  for i, p in enumerate(p_list):
    idx_list[p] = i

  for _ in range(Q):
    a = int(input())
    idx = idx_list[a]
    p_list[idx] = -1
    p_list.append(a)
    idx_list[a] = len(p_list) - 1

  ans_list = []
  for p in p_list:
    if p > 0:
      ans_list.append(p)

  print(*ans_list)

if __name__ == "__main__":
  main()