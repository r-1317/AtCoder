import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

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


# 種を適切な位置に植える
def plant(seed_list):
  field = [[0] * n for _ in range(n)]  # 畑の初期化

  # 種の評価項目のリストをソート(ソート方法は以下から選択)
  plant_list = sort01(seed_list)  
  # seed_list = sort02(seed_list)
  
  ic(plant_list)

  # 良い種ほど畑の中心に植える
  coord_list = [(2,2), (2,3), (3,2), (3,3), (1,2), (2,1), (1,3), (2,4), (3,1), 
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
  global n, m, t
  n, m, t = 6, 15, 10

  seed_list = [list(map(int, input().split())) for _ in range(60)]  # 種の評価項目リスト
  
  ic(seed_list)

if __name__ == "__main__":
  main()