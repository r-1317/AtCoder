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

D = 5  # 貪欲法での深さ

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
    max_root = None
    max_is_leaf_list = [False]*n
    max_height_list = [-1]*n
    max_child_list = [[] for _ in range(n)]
    for root in root_queue:
      tmp_ans = 0
      tmp_ans_list = ans_list[:]
      tmp_serched_list = serched_list[:]
      tmp_serched_count = serched_count
      tmp_is_lesf_list = [False]*n
      tmp_height_list = [-1]*n
      tmp_child_list = [[] for _ in range(n)]
      # queue = [root]
      tmp_ans += a_list[root]
      tmp_ans_list[root] = -1
      tmp_serched_list[root] = True
      tmp_serched_count += 1
      tmp_is_lesf_list[root] = True
      tmp_height_list[root] = 0
      prev_v = root
      # D回まで美しさが最も低い頂点を探索
      for _ in range(D):
        min_a = 10**9
        min_v = None
        # 隣接する頂点の中で最も美しさが低い頂点を探す
        for v in adj_list[prev_v]:
          if not tmp_serched_list[v] and a_list[v] < min_a:
            min_a = a_list[v]
            min_v = v
        # 隣接する頂点がすべて探索済みの場合は終了
        if min_v is None:
          break
        tmp_ans_list[min_v] = prev_v
        tmp_serched_list[min_v] = True
        tmp_serched_count += 1
        tmp_is_lesf_list[min_v] = True
        tmp_height_list[min_v] = 1
        tmp_child_list[prev_v].append(min_v)
        tmp_is_lesf_list[prev_v] = False
        prev_v = min_v
      queue = [prev_v]
      # 深さh(10)までBFS
      for j in range(D, h):
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
    is_leaf_list = max_is_leaf_list
    height_list = max_height_list
    child_list = max_child_list
    leaf_list = []
    for i in range(n):
      if is_leaf_list[i]:
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
          if height_list[leaf] <= height_list[u] < h:
            # もとの親の子から削除
            child_list[ans_list[leaf]].remove(leaf)
            # もとの親の子がなくなったら、葉にする
            if not child_list[ans_list[leaf]]:
              leaf_list.append(ans_list[leaf])
            # 高さを更新
            height_list[leaf] = height_list[u] + 1
            # 子を更新
            child_list[u].append(leaf)
            # uが葉でなくなったら、葉リストから削除
            if u in leaf_list:  # ここの計算量は削減できる
              leaf_list.remove(u)
            # 親をuに変更
            ans_list[leaf] = u
            flag = True

  # 答えを出力
  print(*ans_list)

  # デバッグ用
  ic(root_list)

  ic(serched_count)


if __name__ == "__main__":
  main()