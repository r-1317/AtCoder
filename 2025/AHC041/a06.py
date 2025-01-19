import os
import time

start_time = time.time()

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

    a = 20  # 上位a個の候補を残す

    # 各根の候補に対して、深さh(10)までBFSを行う
    # max_tmp_ans = 0
    # max_tmp_ans_list = []
    # max_tmp_serched_list = []
    # max_tmp_serched_count = 0
    # max_root = None
    # max_is_leaf_list = [False]*n
    # max_height_list = [-1]*n
    # max_child_list = [[] for _ in range(n)]
    better_tmp_ans = [0] * a
    better_tmp_ans_list = [[] for _ in range(a)]
    better_tmp_serched_list = [[] for _ in range(a)]
    better_tmp_serched_count = [0] * a
    better_root = [None] * a
    better_is_leaf_list = [[False]*n for _ in range(a)]
    better_height_list = [[-1]*n for _ in range(a)]
    better_child_list = [[[] for _ in range(n)] for _ in range(a)]
    for root in root_queue:
      tmp_ans = 0
      tmp_ans_list = ans_list[:]
      tmp_serched_list = serched_list[:]
      tmp_serched_count = serched_count
      tmp_is_lesf_list = [False]*n
      tmp_height_list = [-1]*n
      tmp_child_list = [[] for _ in range(n)]
      queue = [root]
      tmp_ans += a_list[root]
      tmp_ans_list[root] = -1
      tmp_serched_list[root] = True
      tmp_serched_count += 1
      tmp_is_lesf_list[root] = True
      tmp_height_list[root] = 0
      for j in range(h):
        next_queue = []
        for u in queue:
          for v in adj_list[u]:
            if not tmp_serched_list[v]:
              tmp_ans += a_list[v] * (h+2)
              tmp_ans_list[v] = u
              tmp_serched_list[v] = True
              tmp_serched_count += 1
              tmp_is_lesf_list[v] = True
              tmp_height_list[v] = j+1
              tmp_child_list[u].append(v)
              next_queue.append(v)
              tmp_is_lesf_list[u] = False
        queue = next_queue
      for k in range(a):
        if better_tmp_ans[k] < tmp_ans:
          better_tmp_ans[k] = tmp_ans
          better_tmp_ans_list[k] = tmp_ans_list
          better_tmp_serched_list[k] = tmp_serched_list
          better_tmp_serched_count[k] = tmp_serched_count
          better_root[k] = root
          better_is_leaf_list[k] = tmp_is_lesf_list
          better_height_list[k] = tmp_height_list
          better_child_list[k] = tmp_child_list
    max_tmp_ans = 0
    for k in range(a):
      # ans_list = max_tmp_ans_list
      # serched_list = max_tmp_serched_list
      # serched_count = max_tmp_serched_count
      # root_list.append(max_root)
      # is_leaf_list = max_is_leaf_list
      # height_list = max_height_list
      # child_list = max_child_list
      tmp_ans_list = better_tmp_ans_list[k]
      # serched_list = better_tmp_serched_list[k]
      # serched_count = better_tmp_serched_count[k]
      # root_list.append(better_root[k])
      tmp_is_leaf_list = better_is_leaf_list[k]
      tmp_height_list = better_height_list[k]
      tmp_child_list = better_child_list[k]
      leaf_list = []
      for i in range(n):
        if tmp_is_leaf_list[i]:
          leaf_list.append(i)
      # ic(height_list)
      # 木の組み換え
      flag = True
      while flag:
        flag = False
        # すべての葉に対して
        for leaf in leaf_list:
          # すべての隣接頂点に対して
          for u in adj_list[leaf]:
            # 高さが自分の高さ以上10未満の場合
            if tmp_height_list[leaf] <= tmp_height_list[u] < h:
              # もとの親の子から削除
              ic(leaf, u)
              ic(tmp_child_list[ans_list[leaf]])
              ic(tmp_ans_list[leaf])
              tmp_child_list[ans_list[leaf]].remove(leaf)
              # もとの親の子がなくなったら、葉にする
              if not tmp_child_list[ans_list[leaf]]:
                leaf_list.append(ans_list[leaf])
              # 高さを更新
              tmp_height_list[leaf] = tmp_height_list[u] + 1
              # 子を更新
              tmp_child_list[u].append(leaf)
              # uが葉でなくなったら、葉リストから削除
              if u in leaf_list:  # ここの計算量は削減できる
                leaf_list.remove(u)
              # 親をuに変更
              ans_list[leaf] = u
              flag = True
      # 美しさの合計を計算
      tmp_ans = 0
      for i in range(n):
        if tmp_height_list[i] != -1:
          tmp_ans += a_list[i] * (tmp_height_list[i]+2)
      if max_tmp_ans < tmp_ans:
        max_tmp_ans = tmp_ans
        max_tmp_ans_list = tmp_ans_list
        max_tmp_serched_list = tmp_serched_list
        max_tmp_serched_count = tmp_serched_count
        max_root = root
        max_is_leaf_list = tmp_is_lesf_list
        max_height_list = tmp_height_list
        max_child_list = tmp_child_list
    ans_list = max_tmp_ans_list
    serched_list = max_tmp_serched_list
    serched_count = max_tmp_serched_count
    root_list.append(max_root)

  # 答えを出力
  print(*ans_list)

  # デバッグ用
  ic(root_list)

  ic(serched_count)


if __name__ == "__main__":
  main()