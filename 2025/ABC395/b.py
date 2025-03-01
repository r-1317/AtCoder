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

  grid = [["" for _ in range(n)] for _ in range(n)]

  for i in range(n):
    j = n - i
    if j < i:
      break
    colour = "#" if i % 2 == 0 else "."  # 想定と逆だが、これが正解
    for x in range(i, j):
      for y in range(i, j):
        grid[x][y] = colour

  for i in range(n):
    print(*grid[i], sep="")

if __name__ == "__main__":
  main()