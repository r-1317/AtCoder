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
  N, M = map(int, input().split())

  ans_list = [0]*N
  for i in range(M):
    ans_list[i%N] += 1

  for a in ans_list:
    print(a)

if __name__ == "__main__":
  main()