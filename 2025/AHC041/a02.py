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
  serched_count = 0  # 探索済み頂点数
  sorted_index = [i for i in range(n)]  # 美しさ順にソートした頂点のindexのリスト
  sorted_index.sort(key=lambda x: a_list[x], reverse=False)  # 美しさが低い順にソート
  tmp_index = 0  # 現在のindex
  ic(sorted_index)

  # デバッグ用
  for i in range(100):
    ic(sorted_index[i*10], a_list[sorted_index[i*10]])

  ans_list = [0]*n  # 親のindexを格納するリスト (根は-1)

  # 未探索の頂点がなくなるまで木を作成
  while serched_count < n:
    tmp_index += 1
    if serched_list[sorted_index[tmp_index]]:  # すでに探索済みの場合
      continue
    root = sorted_index[tmp_index]  # 根
    ic(root)
    ans_list[root] = -1  # 根なので-1
    serched_list[root] = True
    serched_count += 1
    # 深さh(10)までBFS
    queue = [root]
    for i in range(h):
      next_queue = []
      for u in queue:
        for v in adj_list[u]:
          if not serched_list[v]:
            ans_list[v] = u
            serched_list[v] = True
            serched_count += 1
            next_queue.append(v)
      queue = next_queue

  # 答えを出力
  print(*ans_list)

if __name__ == "__main__":
  main()