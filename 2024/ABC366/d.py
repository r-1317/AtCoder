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
  a_list =[ [list(map(int, input().split())) for _ in range(n)] for _ in range(n)]

  m = int(input())  # クエリの数

  q_list = [list(map(int, input().split())) for _ in range(m)]

  sum_list = [[[0]*(n+1) for _ in range(n+1)] for _ in range(n+1)]

  

if __name__ == "__main__":
  main()