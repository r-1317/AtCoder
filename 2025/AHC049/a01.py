import os
import sys
from typing import Tuple, List

MyPC = os.path.basename(__file__) != "Main.py"
# MyPC = False
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

N = 20  # 固定

# 高橋くんの現在位置から目標位置へ移動するための一歩を決定する。
def step_to(takahashi: List[int], target: Tuple[int, int]) -> Tuple[str, List[int]]:
  if takahashi[0] < target[0]:  # 下に移動
    takahashi[0] += 1
    return "D", takahashi
  elif takahashi[0] > target[0]:  # 上に移動
    takahashi[0] -= 1
    return "U", takahashi
  elif takahashi[1] < target[1]:  # 右に移動
    takahashi[1] += 1
    return "R", takahashi
  elif takahashi[1] > target[1]:  # 左に移動
    takahashi[1] -= 1
    return "L", takahashi
  else:  # 到達済み
    return "", takahashi

# 高橋くんが目標位置に到達するまでの動きをリストで返す。
def move_to(takahashi: List[int], target: Tuple[int, int]) -> List[str]:
  ans = []
  # 目標位置に到達するまでループ
  while takahashi[0] != target[0] or takahashi[1] != target[1]:
    step, takahashi = step_to(takahashi, target)
    ans.append(step)  # 動きを追加
  return ans

def main():
  _ = input()  # Nの入力だが、0で固定
  w_list = [list(map(int, input().split())) for _ in range(N)]  # 重さのリスト
  d_list = [list(map(int, input().split())) for _ in range(N)]  # 耐久値のリスト

  takahashi = [0, 0]  # 高橋くんの位置

  ans_list = []  # 動きのリスト

  for i in range(N):
    for j in range(N):
      if w_list[i][j] > 0:
        target = (i, j)  # 目標位置を設定
        # 目的のダンボール箱に到達するまでの動きを追加
        ans_list.extend(move_to(takahashi, target))  # 高橋くんの位置を目標位置に移動
        takahashi[0], takahashi[1] = target  # 高橋くんの位置を更新
        ans_list.append("1")  # ダンボール箱を持ち上げる
        # 原点に戻るための動きを追加
        target = (0, 0)
        ans_list.extend(move_to(takahashi, target))
        takahashi[0], takahashi[1] = target
  
  # 出力
  for ans in ans_list:
    if ans:  # 空文字列でない場合のみ出力
      print(ans)
    else:  # 空文字列は標準エラー出力
      print("空文字列", file=sys.stderr)

  # MyPCのみ、総スコアを出力
  if MyPC:
    t = 0
    for ans in ans_list:
      if ans == "U" or ans == "D" or ans == "L" or ans == "R":
        t += 1
    total_score = N**2 + 2 * N**3 - t  # スコア計算
    print(f"総スコア: {total_score}", file=sys.stderr)



if __name__ == "__main__":
  main()