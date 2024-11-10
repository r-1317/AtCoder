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

  # サバを囲う四角形を作る
  max = -10**5
  best = []

  for i in range(20):
    for j in range(20):
      for k in range(i, 20):
        for l in range(j, 20):
          sum = 0
          for x in range(i, k+1):
            for y in range(j, l+1):
              sum += grid_list[x][y]
          if sum > max:
            max = sum
            best = [i, j, k, l]

  x1 = best[0]*5000
  y1 = best[1]*5000
  x2 = best[2]*5000 + 4999
  y2 = best[3]*5000 + 4999

  print(4)
  print(x1, y1)
  print(x1, y2)
  print(x2, y2)
  print(x2, y1)


if __name__ == "__main__":
  main()