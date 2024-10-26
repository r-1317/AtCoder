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
  grid_list = [(input()) for _ in range(8)]

  x_list = [False] * 8
  y_list = [False] * 8

  for i in range(8):
    for j in range(8):
      if grid_list[i][j] == "#":
        x_list[i] = True
        y_list[j] = True

  ic(x_list)
  ic(y_list)

  ans = 0

  for i in range(8):
    for j in range(8):
      if not(x_list[i] or y_list[j]):
        ans += 1

  print(ans)

if __name__ == "__main__":
  main()