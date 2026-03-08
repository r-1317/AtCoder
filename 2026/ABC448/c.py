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
  a_list = list(map(int, input().split()))
  idx_list = list(range(1, N+1))
  idx_list.sort(key=lambda x: a_list[x-1])

  ic(idx_list)

  for _ in range(Q):
    K = int(input())
    b_list = list(map(int, input().split()))
    b_set = set(b_list)
    for idx in idx_list:
      if idx not in b_set:
        print(a_list[idx-1])
        break

if __name__ == "__main__":
  main()