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
  l_r_list = [list(map(int, input().split())) for _ in range(M)]
  Q = int(input())

  for _ in range(Q):
    s, t = map(int, input().split())

if __name__ == "__main__":
  main()