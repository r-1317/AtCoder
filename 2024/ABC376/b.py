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
  n, q = map(int, input().split())

  hands_list = [1,2]  # 左手、右手の位置
  ans = 0

  for _ in range(q):
    h, t = input().split()
    hand = 0 if h == "L" else 1
    t = int(t)
    cost_list = [0, 0]  # 減少方向、増加方向のコスト
    prev_hands_list = hands_list[:]

    # 減少方向
    while hands_list[hand] != t:
      hands_list[hand] -= 1
      if hands_list[hand] < 1:
        hands_list[hand] = n
      cost_list[0] += 1
      if hands_list[0] == hands_list[1]:  # 両手が同じ位置になったら終了
        cost_list[0] += 10**9
        break
      ic(hands_list)

    # 増加方向
    hands_list = prev_hands_list[:]
    while hands_list[hand] != t:
      hands_list[hand] += 1
      if n < hands_list[hand]:
        hands_list[hand] = 1
      cost_list[1] += 1
      if hands_list[0] == hands_list[1]:  # 両手が同じ位置になったら終了
        cost_list[1] += 10**9
        break
      ic(hands_list)

    hands_list[hand] = t

    ic(h, t)
    ic(cost_list, hands_list)

    ans += min(cost_list)

  print(ans)

if __name__ == "__main__":
  main()