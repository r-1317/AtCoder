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
  n, m, h = map(int, input().split())  # 頂点の数(1000固定), 辺の数(1000^3000), 最大の高さ(10固定)
  a_list = list(map(int, input().split()))  # 各頂点美しさ
  adj_list = [[] for _ in range(n)]  # 隣接リスト
  for _ in range(m):
    u, v = map(int, input().split())
    adj_list[u].append(v)
    adj_list[v].append(u)
  # この後に座標の入力もあるが、使わないので受け取らない

  serched_list = [False] * n  # 探索済みリスト
  sorted_index = [i for i in range(n)]  # 美しさ順にソートした頂点のindexのリスト
  sorted_index.sort(key=lambda x: a_list[x], reverse=True)  # 美しさ順にソート
  tmp_index = 0  # 現在のindex

if __name__ == "__main__":
  main()