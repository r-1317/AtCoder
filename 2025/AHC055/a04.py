import os
from typing import Tuple, List
import sys

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

N = 200

# 現在持っている武器の中から、宝箱box_indexに対する攻撃力が最も高い武器のインデックスを返す
def best_weapon(owned_weapons: List[int], suitableness_matrix: List[List[int]], box_index: int) -> int:
  best_wpn = -1  # 最適な武器のインデックス。初期値は-1（素手攻撃）
  best_power = 1  # 最適な攻撃力。初期値は1（素手攻撃の攻撃力）
  for wpn in owned_weapons:
    power = suitableness_matrix[wpn][box_index]
    if power > best_power:
      best_power = power
      best_wpn = wpn
  return best_wpn

# 武器weapon_indexを使って宝箱box_indexを攻撃する
def use_weapon(owned_weapons: List[int], weapon_index: int, box_index: int, weapon_hp_list: List[int], box_hp_list: List[int], suitableness_matrix: List[List[int]]) -> str:
  # 指定された武器を持っていない場合は素手攻撃。本来はありえないはずだが念のため。
  if (weapon_index not in owned_weapons) and (weapon_index != -1):
    print(f"武器{weapon_index}を所持していません。素手攻撃を行います。", file=sys.stderr)
    return f"-1 {box_index}"  # 素手攻撃コマンドを返す
  # 武器を使用
  attack_power = suitableness_matrix[weapon_index][box_index]  # 武器の攻撃力
  box_hp_list[box_index] -= attack_power  # 宝箱の耐久値を減少
  weapon_hp_list[weapon_index] -= 1  # 武器の耐久値を減少
  # 宝箱の耐久値が0以下なら破壊し、武器を入手
  if box_hp_list[box_index] <= 0:
    owned_weapons.append(box_index)  # 宝箱のインデックスを武器として所持リストに追加
  # 武器の耐久値が0以下なら破壊
  if weapon_hp_list[weapon_index] <= 0:
    owned_weapons.remove(weapon_index)  # 武器を所持リストから削除。計算量がO(N)になるが、N=200なので許容範囲
  return f"{weapon_index} {box_index}"  # 攻撃コマンドを返す

# 所持している武器の中から、最も効果的な攻撃ができる宝箱と武器の組み合わせを返す
def owned_best_pair(box_hp_list: List[int], weapon_hp_list: List[int], suitableness_matrix: List[List[int]], owned_weapons: List[int]) -> Tuple[int, int]:
  best_box = -1
  best_weapon = -2  # -1は素手攻撃を意味するため、-2に設定
  best_effective_power = -1
  for box_index in range(N):
    if box_hp_list[box_index] <= 0:
      continue  # すでに開いている宝箱はスキップ
    for weapon_index in owned_weapons:
      attack_power = suitableness_matrix[weapon_index][box_index]
      effective_power = min(attack_power, box_hp_list[box_index])
      if effective_power > best_effective_power:
        best_effective_power = effective_power
        best_box = box_index
        best_weapon = weapon_index
  return best_box, best_weapon

# まだ一度も開けていない宝箱の中から、最大攻撃力が最も高い宝箱のインデックスを返す
def never_opened_best_pair(box_hp_list: List[int], suitableness_matrix: List[List[int]]) -> int:
  best_box = -1
  best_power = -1
  for box_index in range(N):
    if box_hp_list[box_index] <= 0:
      continue  # すでに開いている宝箱はスキップ
    max_power = -1
    for weapon_index in range(N):
      attack_power = suitableness_matrix[weapon_index][box_index]
      if attack_power > max_power:
        max_power = attack_power
    if max_power > best_power:
      best_power = max_power
      best_box = box_index
  return best_box

# 耐久値が最も低い宝箱のインデックスを返す
def weakest_box(box_hp_list: List[int]) -> int:
  weakest_index = -1
  weakest_hp = 10**9
  for box_index in range(N):
    if box_hp_list[box_index] <= 0:
      continue  # すでに開いている宝箱はスキップ
    if box_hp_list[box_index] < weakest_hp:
      weakest_hp = box_hp_list[box_index]
      weakest_index = box_index
  return weakest_index


def main():
  _ = int(input())  # Nの読み込みだが、200で固定
  box_hp_list = list(map(int, input().split()))  # 宝箱iの残り耐久値のリスト
  weapon_hp_list = list(map(int, input().split()))  # 武器iの耐久値のリスト
  weapon_hp_list.append(10**9)  # indexが-1として扱われる素手攻撃の耐久値を無限大に設定
  suitableness_matrix = [list(map(int, input().split())) for _ in range(N)]  # [i][j]: 武器iの宝箱jに対する攻撃力
  suitableness_matrix.append([1] * N)  # [-1]を素手攻撃用に追加。攻撃力はすべて1に設定

  owned_weapons: List[int] = []
  open_count = 0

  # すべての宝箱が開くまでループ
  while open_count < N:
    # 武器が残っている場合は、最も攻撃力が高くなる組み合わせを選択して使用
    if owned_weapons:
      box_index, weapon_index = owned_best_pair(box_hp_list, weapon_hp_list, suitableness_matrix, owned_weapons)  # 最適な宝箱と武器の組み合わせを取得
      command = use_weapon(owned_weapons, weapon_index, box_index, weapon_hp_list, box_hp_list, suitableness_matrix)
      print(command)
    # 武器が残っていない場合は、耐久値が最も低い宝箱を選択し、素手攻撃を行う
    else:
      box_index = weakest_box(box_hp_list)  # 耐久値が最も低い宝箱のインデックスを取得
      command = use_weapon(owned_weapons, -1, box_index, weapon_hp_list, box_hp_list, suitableness_matrix)
      print(command)

    # 宝箱が開いたかどうかを確認
    if box_hp_list[box_index] <= 0:
      open_count += 1

if __name__ == "__main__":
  main()