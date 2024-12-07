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
  h, w, d = map(int, input().split())
  tmp_grid_list = [list(input()) for _ in range(h)]
  grid_list = [["#"]*(w+2) for _ in range(h+2)]
  # 上下左右に壁を設ける
  for i in range(h):
    for j in range(w):
      grid_list[i+1][j+1] = tmp_grid_list[i][j]

  ans = 0
  prev_coord_list = []

  # 加湿器の座標を0とする
  for i in range(h+2):
    for j in range(w+2):
      if grid_list[i][j] == "H":
        grid_list[i][j] = 0
        ans += 1
        prev_coord_list.append((i, j))

  for i in range(d):
    coord_list = []
    for x, y in prev_coord_list:
      for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_x = x + dx
        new_y = y + dy
        if grid_list[new_x][new_y] == ".":
          grid_list[new_x][new_y] = i + 1
          coord_list.append((new_x, new_y))
          ans += 1
    prev_coord_list = coord_list

  print(ans)

  if MyPC:
    for i in range(h+2):
      print(*grid_list[i], sep="")

if __name__ == "__main__":
  main()