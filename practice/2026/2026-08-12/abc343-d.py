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
  N, T = map(int, input().split())

  score_list = [0]*N
  count_dict = dict()
  count_dict[0] = N
  ans = 1  # 得点0のぶん

  for _ in range(T):
    a, delta_b = map(int, input().split())
    a -= 1  # 0-indexedに揃える
    prev_b = score_list[a]
    score_list[a] += delta_b
    new_b = score_list[a]
    count_dict[prev_b] -= 1
    if count_dict[prev_b] == 0:  # スコアの数を減らす
      ans -= 1

    if not new_b in count_dict:  # count_dictに無ければ初期化
      count_dict[new_b] = 0
    if count_dict[new_b] == 0:
      ans += 1
    count_dict[new_b] += 1

    ic(ans)
    print(ans)


if __name__ == "__main__":
  main()