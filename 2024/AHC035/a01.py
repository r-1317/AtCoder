import os
import numpy as np

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def cos_sim(v1, v2):
  return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

#  評価項目の平均以下が少ない順にソート
def sort01(seed_list):
  avg_list = [0]*m  # 種の評価項目の平均リスト

  for i in range(m):
    avg_list[i] = sum([seed_list[j][i] for j in range(60)]) / 60  # 評価項目の平均値を計算

  ic(avg_list)

  score_list = [[i, 0] for i in range(60)]  # 種の平均より上の評価項目の数リスト

  for i in range(60):
    for j in range(m):
      if avg_list[j] < seed_list[i][j]:
        score_list[i][1] += 1

  ic(score_list)

  score_list.sort(key=lambda x: x[1], reverse=True)  # 評価項目の平均より上の数が多い順にソート

  ic(score_list)

  plant_list = [0]*60  # 良い順にソートされた種のリスト

  for i in range(60):
    plant_list[i] = score_list[i][0]

  return plant_list

# 種の性能の総和が大きい順にソート
def sort02(seed_list):
  score_list = [[i, 0] for i in range(60)]  # 種の性能の総和リスト

  for i in range(60):
    score_list[i][1] = sum(seed_list[i])

  ic(score_list)

  score_list.sort(key=lambda x: x[1], reverse=True)  # 種の性能の総和が大きい順にソート

  ic(score_list)

  plant_list = [0]*60  # 良い順にソートされた種のリスト

  for i in range(60):
    plant_list[i] = score_list[i][0]

  return plant_list

# 種の性能の各項目の平均との差の2乗にもとの符号をつけたものが大きい順にソート
def sort03(seed_list):
  avg_list = [0]*m  # 種の評価項目の平均リスト

  for i in range(m):
    avg_list[i] = sum([seed_list[j][i] for j in range(60)]) / 60  # 評価項目の平均値を計算

  ic(avg_list)

  score_list = [[i, 0] for i in range(60)]  # 種の評価項目の平均との差の2乗リスト

  for i in range(60):
    for j in range(m):
      score_list[i][1] += (seed_list[i][j] - avg_list[j]) * abs((seed_list[i][j] - avg_list[j]))

  ic(score_list)

  score_list.sort(key=lambda x: x[1], reverse=True)  # 種の評価項目の平均との差の2乗が大きい順にソート

  ic(score_list)

  plant_list = [0]*60  # 良い順にソートされた種のリスト

  for i in range(60):
    plant_list[i] = score_list[i][0]

  return plant_list

# 種の性能の各項目の平均との差と0の大きい方の2乗が大きい順にソート
def sort04(seed_list):
  avg_list = [0]*m  # 種の評価項目の平均リスト

  for i in range(m):
    avg_list[i] = sum([seed_list[j][i] for j in range(60)]) / 60  # 評価項目の平均値を計算

  ic(avg_list)

  score_list = [[i, 0] for i in range(60)]  # 種の評価項目の平均との差の2乗リスト

  for i in range(60):
    for j in range(m):
      score_list[i][1] += max((seed_list[i][j] - avg_list[j]),0) ** 2

  ic(score_list)

  score_list.sort(key=lambda x: x[1], reverse=True)  # 種の評価項目の平均との差の2乗が大きい順にソート

  ic(score_list)

  plant_list = [0]*60  # 良い順にソートされた種のリスト

  for i in range(60):
    plant_list[i] = score_list[i][0]

  return plant_list

# cosine類似度を使用してソート
def sort05(seed_list):
  avg_list = [0]*m  # 種の評価項目の平均リスト

  for i in range(m):
    avg_list[i] = sum([seed_list[j][i] for j in range(60)]) / 60  # 評価項目の平均値を計算

  ic(avg_list)

  score_list = [[i, 0] for i in range(60)]  # 種の評価項目の平均との差の2乗リスト

  for i in range(60):
    for j in range(m):
      score_list[i][1] += max((seed_list[i][j] - avg_list[j]),0) ** 2

  ic(score_list)

  score_list.sort(key=lambda x: x[1], reverse=True)  # 種の評価項目の平均との差の2乗が大きい順にソート

  ic(score_list)

  plant_list = [0]*60  # 良い順にソートされた種のリスト

  for i in range(60):
    plant_list[i] = score_list[i][0]

  # ここからcosine類似度を使用してソート
  top5_list = np.array([seed_list[i] for i in plant_list[:5]])  # 上位5個の種の評価項目リスト
  ic(top5_list)

  cos_sim_list = [[i, -1] for i in plant_list[:5]]  # cosine類似度リスト

  for i in range(5):
    for j in range(5):
      cos_sim_list[i][1] += cos_sim(top5_list[i], top5_list[j])

  ic(cos_sim_list)

  cos_sim_list.sort(key=lambda x: x[1])  # cosine類似度が小さい順にソート

  ic(cos_sim_list)

  for i in range(5):
    plant_list[i] = cos_sim_list[i][0]

  ic(plant_list)

  return plant_list

# 種を適切な位置に植える
def plant(seed_list):
  field = [[0] * n for _ in range(n)]  # 畑の初期化

  # 種の評価項目のリストをソート(ソート方法は以下から選択)
  # plant_list = sort01(seed_list)  
  # plant_list = sort02(seed_list)
  # plant_list = sort03(seed_list)
  # plant_list = sort04(seed_list)
  plant_list = sort05(seed_list)
  
  ic(plant_list)

  # 良い種ほど畑の中心に植える (今のところ最も良い)
  coord_list = [(2,2), (2,3), (3,2), (3,3), (1,2), (2,1), (1,3), (2,4), (3,1), 
                (4,2), (3,4), (4,3), (1,1), (1,4), (4,1), (4,4), (0,2), (2,0), 
                (0,3), (2,5), (3,0), (5,2), (3,5), (5,3), (0,1), (1,0), (0,4), 
                (1,5), (4,0), (5,1), (4,5), (5,4), (0,0), (0,5), (5,0), (5,5)]

  # # いい種ほど畑の左上に植える
  # coord_list = [(0,0), (0,1), (1,0), (1,1), (0,2), (2,0), (1,2), (2,1), (0,3),
  #               (3,0), (2,2), (1,3), (3,1), (0,4), (4,0), (2,3), (3,2), (1,4),
  #               (4,1), (0,5), (5,0), (3,3), (2,4), (4,2), (1,5), (5,1), (3,4),
  #               (4,3), (2,5), (5,2), (4,4), (3,5), (5,3), (4,5), (5,4), (5,5)]

  # # いい種ほど畑の中心に植える(改良版)(性能は低下していた)
  # coord_list = [(2,2), (1,2), (2,1), (2,3), (3,2), (1,1), (1,3), (3,1), (3,3),
  #               (0,2), (2,0), (2,4), (4,2), (0,1), (1,0), (0,3), (1,4), (3,0),
  #               (4,1), (3,4), (4,3), (0,0), (0,4), (4,0), (4,4), (2,5), (5,2),
  #               (1,5), (5,1), (3,5), (5,3), (0,5), (5,0), (4,5), (5,4), (5,5)]

  # cosine類似度を使用する際の座標リスト
  coord_list = [(2,2), (2,3), (3,2), (2,1), (1,2), (3,3), (1,3), (2,4), (3,1), 
                (4,2), (3,4), (4,3), (1,1), (1,4), (4,1), (4,4), (0,2), (2,0), 
                (0,3), (2,5), (3,0), (5,2), (3,5), (5,3), (0,1), (1,0), (0,4), 
                (1,5), (4,0), (5,1), (4,5), (5,4), (0,0), (0,5), (5,0), (5,5)]
  
  # 種を畑に植える
  for i in range(36):
    x, y = coord_list[i]
    field[x][y] = plant_list[i]

  ic(field)

  return field


def main():
  global n, m, t  # n: 畑の行と列の数, m: 種の評価項目の数, t: 年数
  n, m, t = map(int, input().split())
  
  for _ in range(t):
    seed_list = [list(map(int, input().split())) for _ in range(60)]  # 種60個の評価項目のリスト
    field = plant(seed_list)
    for i in range(n):
      print(*field[i])

    # デバッグ用
    if MyPC:
      print("---Debug---")

      avg_list = [0]*m  # 種の評価項目の平均リスト
      for i in range(m):
        avg_list[i] = sum([seed_list[j][i] for j in range(60)]) / 60  # 評価項目の平均値を計算

      score_list = [[i, 0] for i in range(60)]  # 種の評価項目の平均との差の2乗リスト

      for i in range(60):
        for j in range(m):
          score_list[i][1] += (seed_list[i][j] - avg_list[j]) * abs((seed_list[i][j] - avg_list[j]))

      for i in range(n):
        for j in range(n):
          print(int(score_list[field[i][j]][1]), end=" ")
        print("")

if __name__ == "__main__":
  main()