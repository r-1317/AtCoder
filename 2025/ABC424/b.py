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
  N, M, K = map(int, input().split())
  
  ac_list = [0] * (N+1)

  ans_list = []

  for _ in range(K):
    a, b = map(int, input().split())
    ac_list[a] += 1
    if ac_list[a] == M:
      ans_list.append(a)

  ic(ans_list)
  print(*ans_list)


if __name__ == "__main__":
  main()