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
  N = int(input())
  adj_list = [[] for _ in range(N)]

  for _ in range(N-1):
    a, b = map(int, input().split())
    

if __name__ == "__main__":
  main()