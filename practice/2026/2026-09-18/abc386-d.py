import os
import bisect

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  N, M = map(int, input().split())
  v_limit_list = [(10**18, 0)]  # xごとの黒になるy
  h_limit_list = [(10**18, 0)]  # yごとの黒になるx

  white_list = []
  x_black_list = []
  y_black_list = []
  for _ in range(M):
    row = input().split()
    x = int(row[0])
    y = int(row[1])
    if row[2] == "W":  # 白の場合は配列に入れて終わり
      white_list.append((x, y))
    else:  # 黒の場合
      x_black_list.append((x, y))
      y_black_list.append((y, x))
      # v_limit_list.append((x, y))
      # h_limit_list.append((y, x))

  white_list.sort()
  x_black_list.sort(reverse=True)
  y_black_list.sort(reverse=True)

  for x, y in x_black_list:
    if v_limit_list[-1][0] == x:  # すでに同じxがある場合は置かない。一番大きいのが最初に置かれているはず
      continue
    v_limit_list.append((x, y))

  for y, x in y_black_list:
    if h_limit_list[-1][0] == y:  # xの時の同様の理由でスキップ
      continue
    h_limit_list.append((y, x))

  v_limit_list = v_limit_list[::-1]
  h_limit_list = h_limit_list[::-1]

  # ic(v_limit_list)

  ans = True
  for x, y in white_list:
    if v_limit_list[bisect.bisect_left(v_limit_list, (x, 0))][1] >= y:
      ans = False
      break
    if h_limit_list[bisect.bisect_left(h_limit_list, (y, 0))][1] >= x:
      ans = False
      break

  print("Yes" if ans else "No")

if __name__ == "__main__":
  main()