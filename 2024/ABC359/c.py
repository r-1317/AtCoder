import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# 現在地から目的地までの距離を計算
def calc_dist(tmp_coord, t_coord):
  distance = [0, 0]  # x, y
  distance[0] = t_coord[0] - tmp_coord[0]
  distance[1] = t_coord[1] - tmp_coord[1]

  # 通行料なしで行ける場合、1マス移動する
  if sum(tmp_coord) % 2 == 1 and distance[0] < 0:
    tmp_coord[0] -= 1
    distance[0] = t_coord[0] - tmp_coord[0]
  elif sum(tmp_coord) % 2 == 0 and 0 < distance[0]:
    tmp_coord[0] += 1
    distance[0] = t_coord[0] - tmp_coord[0]

  return distance, tmp_coord

def main():
  s_coord = list(map(int, input().split()))  # 開始地点の座標
  t_coord = list(map(int, input().split()))  # 目的地の座標

  tmp_coord = s_coord[:]

  # 開始地点から目的地までの距離を計算
  distance, tmp_coord = calc_dist(tmp_coord, t_coord)

  ic(tmp_coord)
  ic(distance)

  ans = 0

  # 斜め移動
  ans = min((abs(distance[0])+1)//2*2, abs(distance[1]))
  ic(ans)

  tmp_coord[0] += ans*(-1 if distance[0] < 0 else 1)
  tmp_coord[1] += ans*(-1 if distance[1] < 0 else 1)

  ic(tmp_coord)

  # 現在地から目的地までの距離を計算
  distance, tmp_coord = calc_dist(tmp_coord, t_coord)

  ic("斜め移動後の座標と距離")
  ic(tmp_coord)
  ic(distance)

  # この時点でxかyのどちらかの距離は0になっている

  # 縦移動
  ans += abs(distance[1])

  # 横移動
  ans += (abs(distance[0])+1)//2
  ic((abs(distance[0])+1)//2)

  print(ans)

  # ic(ans == main_2(s_coord, t_coord))

if __name__ == "__main__":
  main()

# メモ
# (x+1)//2