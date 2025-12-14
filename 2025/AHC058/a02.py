import os
import numpy as np
from typing import Tuple, List

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

N = 10  # 機械のIDの種類数。10固定
L = 4  # 機械のLevelの種類数。4固定
T = 500  # ターン数。500固定
K = 1 # 初期のりんごの数。1固定

X = 3.0  # 評価関数に用いる値。可変
ic(X)

def predict_result(turn: int, apple_num: int, apple_production_list: List[int], machine_count_list: List[List[int]], power_list: List[List[int]]) -> int:
  """
  現在の状態から最終ターンまで進めたときに得られるりんごの数を予測する関数

  Args:
    turn (int): 現在のターン数
    apple_num (int): 現在のりんごの数
    apple_production_list (List[int]): 各機械IDで各ターンに生産されるりんごの数のリスト
    cost_list (List[List[int]]): 各機械IDとレベルでの強化コストのリスト
    machine_count_list (List[List[int]]): 各機械IDとレベルでの台数のリスト
    power_list (List[List[int]]): 各機械IDとレベルでの生産力のリスト

  Returns:
    int: 最終的に得られるりんごの数
  """

  # この関数は「これ以降は強化を一切行わない（毎ターン -1 を出す）」という
  # 仮定のもと、残りターンをそのままシミュレーションして最終りんご数を返す。
  # 呼び出し元の状態を破壊しないようにコピーして計算する。
  apples = apple_num

  # 状態のコピーを作成
  machine_counts: List[List[int]] = [row[:] for row in machine_count_list]
  powers = [row[:] for row in power_list]

  # ターン進行：行動(なし) → Level 0..L-1 の順に処理
  for _t in range(turn, T):
    # Level 0: りんご生産
    for j in range(N):
      apples += apple_production_list[j] * machine_counts[0][j] * powers[0][j]

    # Level 1..: 下位レベルの台数増加
    for i in range(1, L):
      for j in range(N):
        machine_counts[i - 1][j] += machine_counts[i][j] * powers[i][j]

  return apples

# 状態を表すクラス
class state:
  def __init__(self, turn: int, apple_num: int, machine_count_list: List[List[int]], power_list: List[List[int]]):
    self.turn = turn
    self.apple_num = apple_num
    self.machine_count_list = machine_count_list
    self.power_list = power_list

  # 状態のコピーを作成するメソッド
  def copy(self):
    return state(
      self.turn,
      self.apple_num,
      [row[:] for row in self.machine_count_list],
      [row[:] for row in self.power_list]
    )
  
  # 現在の状態から最終ターンまで進めたときに得られるりんごの数を予測するメソッド
  def result(self, apple_production_list: List[int]) -> int:
    return predict_result(self.turn, self.apple_num, apple_production_list, self.machine_count_list, self.power_list)
  
  def enpower(self, machine_id: int, level: int, cost_list: List[List[int]]) -> bool:
    """
    指定された機械IDとレベルで強化を行うメソッド

    Args:
      machine_id (int): 強化する機械のID
      level (int): 強化する機械のレベル
      cost_list (List[List[int]]): 各機械IDとレベルでの強化コストのリスト

    Returns:
      bool: 強化が成功したかどうか
    """
    cost = cost_list[level][machine_id] * (self.power_list[level][machine_id] + 1)  # 強化コストを計算
    if self.apple_num >= cost:
      self.apple_num -= cost
      self.power_list[level][machine_id] += 1
      return True  # 強化成功
    else:
      return False  # 強化失敗
    
  def can_enpower(self, machine_id: int, level: int, cost_list: List[List[int]]) -> bool:
    """
    指定された機械IDとレベルで強化が可能かどうかを判定するメソッド

    Args:
      machine_id (int): 強化する機械のID
      level (int): 強化する機械のレベル
      cost_list (List[List[int]]): 各機械IDとレベルでの強化コストのリスト

    Returns:
      bool: 強化が可能かどうか
    """
    cost = cost_list[level][machine_id] * (self.power_list[level][machine_id] + 1)  # 強化コストを計算
    return self.apple_num >= cost
  
  def step(self, apple_production_list: List[int]):
    """
    1ターン進行するメソッド

    Args:
      apple_production_list (List[int]): 各機械IDで各ターンに生産されるりんごの数のリスト
    """
    # Level 0: りんご生産
    for j in range(N):
      self.apple_num += apple_production_list[j] * self.machine_count_list[0][j] * self.power_list[0][j]

    # Level 1..: 下位レベルの台数増加
    for i in range(1, L):
      for j in range(N):
        self.machine_count_list[i - 1][j] += self.machine_count_list[i][j] * self.power_list[i][j]

    # ターン数を進める
    self.turn += 1

def predixt_increase(turn: int, apple_num: int, apple_production_list: List[int], machine_count_list: List[List[int]], power_list: List[List[int]], machine_id: int, level: int) -> int:
  """
  指定された機械IDとレベルで強化を行った場合の最終的に得られるりんごの数の増加量を予測する関数
  指定されたIDのみを調べることで、predict_result関数よりも計算量を削減することができる。

  Args:
    turn (int): 現在のターン数
    apple_num (int): 現在のりんごの数
    apple_production_list (List[int]): 各機械IDで各ターンに生産されるりんごの数のリスト
    cost_list (List[List[int]]): 各機械IDとレベルでの強化コストのリスト
    machine_count_list (List[List[int]]): 各機械IDとレベルでの台数のリスト
    power_list (List[List[int]]): 各機械IDとレベルでの生産力のリスト
    machine_id (int): 強化する機械のID
    level (int): 強化する機械のレベル

  Returns:
    int: 最終的に得られるりんごの数の増加量
  """

  # この関数は「これ以降は強化を一切行わない（毎ターン -1 を出す）」という
  # 仮定のもと、残りターンをそのままシミュレーションして最終りんご数を返す。
  # 呼び出し元の状態をコピーすると計算量が増えるため、指定されたIDのみを調べることで計算量を削減する。
  
  # まずは強化前の最終りんご数を計算
  prev_apples = 0
  machine_counts = [1, 1, 1, 1]  # 指定されたIDの各レベルの台数を格納するリスト
  # powers = [0, 0, 0, 0]  # 指定されたIDの各レベルの生産力を格納するリスト
  powers = [power_list[i][machine_id] for i in range(L)]  # 指定されたIDの各レベルの生産力を格納するリスト
  # powers[level] = power_list[level][machine_id] + 1  # 指定されたレベルの強化後の生産力を設定

  # ターン進行：行動(なし) → Level 0..L-1 の順に処理
  for _t in range(turn, T):
    # Level 0: りんご生産
    prev_apples += apple_production_list[machine_id] * machine_counts[0] * powers[0]

    # Level 1..: 下位レベルの台数増加
    for i in range(1, L):
      machine_counts[i - 1] += machine_counts[i] * powers[i]

  # 次に強化後の最終りんご数を計算
  next_apples = 0
  machine_counts = [1, 1, 1, 1]  # 指定されたIDの各レベルの台数を格納するリスト
  powers = [power_list[i][machine_id] for i in range(L)]  # 指定されたIDの各レベルの生産力を格納するリスト
  powers[level] = power_list[level][machine_id] + 1  # 指定されたレベルの強化後の生産力を設定

  # ターン進行：行動(なし) → Level 0..L-1 の順に処理
  for _t in range(turn, T):
    # Level 0: りんご生産
    next_apples += apple_production_list[machine_id] * machine_counts[0] * powers[0]

    # Level 1..: 下位レベルの台数増加
    for i in range(1, L):
      machine_counts[i - 1] += machine_counts[i] * powers[i]

  return next_apples - prev_apples

def calc_score(apple_num: int) -> int:
  """
  最終的に得られるりんごの数からスコアを計算する関数

  Args:
    apple_num (int): 最終的に得られるりんごの数

  Returns:
    int: スコア
  """
  return round(10**5 * np.log2(apple_num))

def sigmoid(x: float) -> float:
  """
  シグモイド関数

  Args:
    x (float): 入力値

  Returns:
    float: シグモイド関数の出力値
  """
  return 1 / (1 + np.exp(-x))

def eval02(apple_num: int, increase: int, turn: int) -> float:
  """
  最終的に得られるりんごの数と増加量からヒューリスティックな評価値を計算する関数

  Args:
    apple_num (int): 最終的に得られるりんごの数
    increase (int): りんごの数の増加量
    turn (int): 現在のターン数

  Returns:
    int: スコア
  """

  # 特別処理: 最初のターンは確実に強化する
  if turn == 0:
    return increase

  return increase  # 基本形

  return increase - turn**3 * 0.01 - turn**2 * 0.1 - turn * 200 - 500

def main():
  _, _, _, _ = map(int, input().split())
  apple_num = K  # りんごの数を初期化
  apple_production_list: List[int] = list(map(int, input().split()))  # IDがjの機械で各ターンで生産されるりんごの数を格納するリスト
  cost_list: List[List[int]] = [list(map(int, input().split())) for _ in range(L)]  # cost_list[i][j]: IDがjでレベルがiの機械を強化するのに必要なりんごの数

  machine_count_list: List[List[int]] = [[1] * N for _ in range(L)]  # machine_count_list[i][j]: IDがjでレベルがiの機械の台数
  power_list: List[List[int]] = [[0] * N for _ in range(L)]  # power_list[i][j]: IDがjでレベルがiの機械の生産力

  turn = 0  # 現在のターン数を初期化
  current_state = state(turn, apple_num, machine_count_list, power_list)  # 現在の状態を表すオブジェクトを作成
  ans_list: List[Tuple[int, int]] = []  # 各ターンで強化した機械IDとレベルの組み合わせを格納するリスト

  # ic(current_state.apple_num)
  # ic(current_state.can_enpower(0, 0, cost_list))
  
  # 各ターンの処理
  # 最終的に得られるりんごの数が最大化となるように貪欲法を用いて強化を行う
  for turn in range(T):
    best_eval = 0.0
    best_machine_id = -1
    best_level = -1

    # 全ての機械IDとレベルの組み合わせを試す
    for machine_id in range(N):
      for level in range(L):
        # 強化が可能かどうかを確認
        if current_state.can_enpower(machine_id, level, cost_list):
          # 強化した場合の最終的に得られるりんごの数の増加量を予測
          increase = predixt_increase(current_state.turn, current_state.apple_num, apple_production_list, current_state.machine_count_list, current_state.power_list, machine_id, level)
          increase -= cost_list[level][machine_id] * (current_state.power_list[level][machine_id] + 1)  # 強化コスト分を差し引く
          next_apple_num = current_state.apple_num - cost_list[level][machine_id] * (current_state.power_list[level][machine_id] + 1)  # 強化コスト分を差し引く

          eval = eval02(next_apple_num, increase, current_state.turn)

          # if turn == 0:
          #   ic((machine_id, level, increase))
          
          # 最も増加量が大きい組み合わせを記録
          if eval > best_eval:
            best_eval = eval
            best_machine_id = machine_id
            best_level = level

    # 最も増加量が大きい組み合わせで強化を行う
    if best_machine_id != -1 and best_level != -1:
      current_state.enpower(best_machine_id, best_level, cost_list)
      # 強化した機械IDとレベルの組み合わせを記録
      ans_list.append((best_level, best_machine_id))
    else:
      # 強化できなかった場合は (-1, -1) を記録
      ans_list.append((-1, -1))

    # 1ターン進行
    current_state.step(apple_production_list)

  # 結果の出力
  for row in ans_list:
    if row == (-1, -1):
      print(-1)  # 出力形式に合わせる
    else:
      print(*row)

  ic(current_state.apple_num)
  ic(calc_score(current_state.apple_num))
  # ic(calc_score(current_state.apple_num)*150)

if __name__ == "__main__":
  main()