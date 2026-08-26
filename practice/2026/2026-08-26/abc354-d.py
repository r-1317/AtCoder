import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

density = [[2, 1, 0, 1],[1, 2, 1, 0]]

def main():
  A, B, C, D = map(int, input().split())

  ans = 0
  dx = C - A
  dy = D - B

  ans += (dx // 4) * (dy // 2) * 8

  rx = dx % 4
  ry = dy % 2

  # 縦方向のあまり
  h_rest = 0
  for i in range(A, A+rx):
    h_rest += density[0][i%4] + density[1][i%4]
  ans += h_rest * (dy // 2)
  if dy % 2 > 0:
    for i in range(A, A+rx): # 縦横共通のあまり
      ans += density[B % 2][i%4]

  # 横方向のあまり
  dx -= rx  # 共通部分を切ったので
  r = dx % 4
  y_idx = B % 2
  v_rest = 0
  for i in range(B, B+ry):
    v_rest += sum(density[i%2])
  ans += v_rest * (dx // 4)
  if dx % 4 > 0:
    for i in range(B, B+r):
      ans += density[y_idx][i%4]

  print(ans)

if __name__ == "__main__":
  main()