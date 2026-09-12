import os
import math

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def dfs(S, pos_list, rest_list, x, y, total_len):
  if not rest_list:
    return total_len

  min_len = float("inf")
  for idx in rest_list:
    for j in range(2):
      xs, ys = pos_list[idx][j*2], pos_list[idx][j*2 + 1]
      xt, yt = pos_list[idx][(j*2 + 2) % 4], pos_list[idx][(j*2 + 3) % 4]
      new_total_len = total_len + math.sqrt((xs - x)**2 + (ys - y)**2) / S
      new_rest_list = rest_list[:]
      new_rest_list.remove(idx)
      min_len = min(min_len, dfs(S, pos_list, new_rest_list, xt, yt, new_total_len))

  return min_len


def main():
  N, S, T = map(int, input().split())

  pos_list = [list(map(int, input().split())) for _ in range(N)]

  # 印字の時間を加算
  ans = 0.0
  for x1, y1, x2, y2 in pos_list:
    ans += math.sqrt((x2 - x1)**2 + (y2 - y1)**2) / T

  ans += dfs(S, pos_list, list(range(N)), 0, 0, 0.0)
  print(ans)

if __name__ == "__main__":
  main()