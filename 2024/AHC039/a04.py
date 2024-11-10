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
  n = int(input())  # 5000固定
  grid_list = [[0]*20 for _ in range(20)]  # 座標を20*20で分割
  
  # サバの座標を追加
  for _ in range(n):
    x, y = map(int, input().split())
    # 10**5の場合は99999にする
    if x == 10**5:
      x = 99999
    if y == 10**5:
      y = 99999
    grid_list[x//5000][y//5000] += 1  # 当該マスに1足す
  
  # イワシの座標を追加
  for _ in range(n):
    x, y = map(int, input().split())
    # 10**5の場合は99999にする
    if x == 10**5:
      x = 99999
    if y == 10**5:
      y = 99999
    grid_list[x//5000][y//5000] -= 1  # 当該マスに1引く

  # 左上のスコアを計算
  score_1 = -10**5
  for x in range(10):
    for y in range(10):
      if grid_list[x][y] > score_1:
        score_1 = grid_list[x][y]

  # 右上のスコアを計算
  score_2 = -10**5
  for x in range(10, 20):
    for y in range(10):
      if grid_list[x][y] > score_2:
        score_2 = grid_list[x][y]

  # 右下のスコアを計算
  score_3 = -10**5
  for x in range(10, 20):
    for y in range(10, 20):
      if grid_list[x][y] > score_3:
        score_3 = grid_list[x][y]

  # 左下のスコアを計算
  score_4 = -10**5
  for x in range(10):
    for y in range(10, 20):
      if grid_list[x][y] > score_4:
        score_4 = grid_list[x][y]

  # ic(score_1, score_2, score_3, score_4)
  max_quarter_score = max(score_1, score_2, score_3, score_4)

  tmp_grid_list = [g[:] for g in grid_list]

  if max_quarter_score == score_1:
    ic("score_1")
  elif max_quarter_score == score_2:
    ic("score_2")
    # 左に90度回転
    for x in range(4):
      for y in range(4):
        grid_list[3-y][x] = tmp_grid_list[x][y]
  elif max_quarter_score == score_3:
    ic("score_3")
    # 180度回転
    for x in range(4):
      for y in range(4):
        grid_list[3-x][3-y] = tmp_grid_list[x][y]
  elif max_quarter_score == score_4:
    ic("score_4")
    # 右に90度回転
    for x in range(4):
      for y in range(4):
        grid_list[y][3-x] = tmp_grid_list[x][y]

  # サバを囲う四角形を作る
  max_score = -10**5
  best = []

  for x_0 in range(20):
    for y_0 in range(20):
      for x_1 in range(x_0, 20):
        for y_1 in range(y_0, 20):
          for x_2 in range(x_1+1, 20):
            for y_2 in range(y_1+1, 20):
              sum = 0
              for x in range(x_0, x_2+1):
                for y in range(y_0, y_2+1):
                  sum += grid_list[x][y]
              for x in range(x_1+1, x_2+1):
                for y in range(y_1+1, y_2+1):
                  sum -= grid_list[x][y]
              if max_score < sum:
                max_score = sum
                best = [x_0, y_0, x_1, y_1, x_2, y_2]

  ic(best)

  # if max_quarter_score == score_2:
  #   best = [y_0, 10**5-x_1, y_1, 10**5-x_2, y_2, 10**5-x_0]
  # elif max_quarter_score == score_3:
  #   best = [10**5 - b for b in best]
  # elif max_quarter_score == score_4:
  #   best = [10**5-y_0, x_0, 10**5-y_1, x_1, 10**5-y_2, x_2]

  ic(best)

  x_0 = best[0]*5000
  y_0 = best[1]*5000
  x_1 = best[2]*5000 + 4999
  y_1 = best[3]*5000 + 4999
  x_2 = best[4]*5000 + 4999
  y_2 = best[5]*5000 + 4999

  if max_quarter_score == score_2:
    x_0, y_0, x_1, y_1, x_2, y_2 = 10**5-y_0, x_0, 10**5-y_1, x_1, 10**5-y_2, x_2
  elif max_quarter_score == score_3:
    x_0, y_0, x_1, y_1, x_2, y_2 = 10**5 - x_0, 10**5 - y_0, 10**5 - x_1, 10**5 - y_1, 10**5 - x_2, 10**5 - y_2
  elif max_quarter_score == score_4:
    x_0, y_0, x_1, y_1, x_2, y_2 = y_0, 10**5-x_0, y_1, 10**5-x_1, y_2, 10**5-x_2

  ic(x_0, y_0, x_1, y_1, x_2, y_2)

  print(6)
  print(x_0, y_0)
  print(x_2, y_0)
  print(x_2, y_1)
  print(x_1, y_1)
  print(x_1, y_2)
  print(x_0, y_2)

if __name__ == "__main__":
  main()