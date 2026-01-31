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
  T = int(input())

  for _ in range(T):
    N, C = map(int, input().split())
    s_list = [list(input()) for _ in range(N)]
    grid = [["#"] + s_list[i] + ["#"] for i in range(N)]
    no_wall_list = [N]*N

    for i in range(1, N+1):
      nw = N
      for j in range(N-1, -1, -1):
        if grid[i] == "#":
          break
        nw = j
      no_wall_list[i] = nw

    takahashi = (N-1, C)

if __name__ == "__main__":
  main()