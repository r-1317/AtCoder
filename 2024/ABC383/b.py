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
  grid_list = [list(input()) for _ in range(h)]
  ans = 0
  # 1つめの加湿器の座標
  for i in range(h*w):
    x_1 = i // w
    y_1 = i % w
    # 2つめの加湿器の座標
    for j in range(i):
      x_2 = j // w
      y_2 = j % w
      # 机がある場合はスキップ
      if grid_list[x_1][y_1] == "#" or grid_list[x_2][y_2] == "#":
        continue
      # 加湿されるマスの個数
      count = 0
      for x in range(h):
        for y in range(w):
          if grid_list[x][y] == "#":
            continue
          # 加湿器1からの距離
          d_1 = abs(x_1 - x) + abs(y_1 - y)
          # 加湿器2からの距離
          d_2 = abs(x_2 - x) + abs(y_2 - y)
          if d_1 <= d or d_2 <= d:
            count += 1
      ans = max(ans, count)
  print(ans)


if __name__ == "__main__":
  main()