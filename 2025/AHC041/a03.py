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
  ans_list = [0] * n  # 親のリスト (根の場合は-1)
  ans_list = [-1] * n  # デバッグ用

  root_queue = []  # 根の候補のキュー
  x = 1000  # 1回の探索での最大の個
  root_list = []  # 実際に根になった頂点のリスト

  # 未探索の頂点がなくなるまで木を作成
  while serched_count < n:
  # while not all(serched_list):  # バグ対策
    # 未探索の頂点をindex順に最大x個queueに入れる
    for i in range(n):
      if not serched_list[i]:
        root_queue.append(i)
      if x <= len(root_queue):
        break

    # 各根の候補に対して、深さh(10)までBFSを行う
    max_tmp_ans = 0
    max_tmp_ans_list = []
    max_tmp_serched_list = []
    max_tmp_serched_count = 0
    max_root = -1
    for root in root_queue:
      tmp_ans = 0
      tmp_ans_list = ans_list[:]
      tmp_serched_list = serched_list[:]
      tmp_serched_count = serched_count
      queue = [root]
      tmp_ans += a_list[root]
      tmp_ans_list[root] = -1
      tmp_serched_list[root] = True
      tmp_serched_count += 1
      for j in range(h):
        next_queue = []
        for u in queue:
          for v in adj_list[u]:
            if not tmp_serched_list[v]:
              tmp_ans += a_list[v] * (h+2)
              tmp_ans_list[v] = u
              tmp_serched_list[v] = True
              tmp_serched_count += 1
              next_queue.append(v)
        queue = next_queue
      if max_tmp_ans < tmp_ans:
        max_tmp_ans = tmp_ans
        max_tmp_ans_list = tmp_ans_list
        max_tmp_serched_list = tmp_serched_list
        max_tmp_serched_count = tmp_serched_count
        max_root = root
    ans_list = max_tmp_ans_list
    serched_list = max_tmp_serched_list
    serched_count = max_tmp_serched_count
    root_list.append(max_root)

  # 答えを出力
  print(*ans_list)

  # デバッグ用
  ic(root_list)

  ic(serched_count)

  ic(serched_list[495])


if __name__ == "__main__":
  main()