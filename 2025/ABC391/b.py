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
  n, m = map(int, input().split())
  s_grid = [list(input()) for _ in range(n)]
  t_grid = [list(input()) for _ in range(m)]

  for a in range(n - m + 1):
    for b in range(n - m + 1):
      for i in range(m):
        for j in range(m):
          if s_grid[a + i][b + j] != t_grid[i][j]:
            break
        else:
          continue
        break
      else:
        print(a+1, b+1)
        exit()

if __name__ == "__main__":
  main()