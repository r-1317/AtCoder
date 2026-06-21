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
  N = int(input())
  h_l_list = [list(map(int, input().split())) for _ in range(N)]
  Q = int(input())
  t_list = list(map(int, input().split()))

  t2_list = [[t, i] for i, t in enumerate(t_list)]

  ic(t2_list)

  t2_list.sort(key=lambda x: x[0])  # 時刻順にソート

  max_list = []  # とりあえず逆順で入れて後でreverseする
  h_l_list.reverse()

  current_max = -1

  # 与えられた逆順で回す
  for h, l in h_l_list:
    current_max = max(current_max, h)
    max_list.append((l, current_max))

  max_list.reverse()  # これで時系列順に戻るはず

  idx = 0

  ans_list = []

  for t, t_idx in t2_list:
    while max_list[idx][0] <= t:
      idx += 1
    
    ans_list.append([max_list[idx][1], t_idx])

  ans_list.sort(key=lambda x: x[1])  # 与えられた順にソート

  for ans, t_idx in ans_list:
    print(ans)

if __name__ == "__main__":
  main()