import os
from sortedcontainers import SortedSet

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  H, W, Q = map(int, input().split())

  h_set_list = [SortedSet(list(range(W)) + [-10**9, 10**9]) for _ in range(H)]
  v_set_list = [SortedSet(list(range(H)) + [-10**9, 10**9]) for _ in range(W)]

  for _ in range(Q):
    x, y = map(int, input().split())
    x -= 1
    y -= 1
    if y in h_set_list[x]:  # そのマスに壁があった場合
      h_set_list[x].discard(y)
      v_set_list[y].discard(x)
    else:
      u = v_set_list[y][v_set_list[y].bisect(x) - 1]
      d = v_set_list[y][v_set_list[y].bisect(x)]
      l = h_set_list[x][h_set_list[x].bisect(y) - 1]
      r = h_set_list[x][h_set_list[x].bisect(y)]

      # ic(x, y)
      # ic(u, d, l, r)

      if u > -1:
        h_set_list[u].discard(y)
        v_set_list[y].discard(u)
      if d < H:
        h_set_list[d].discard(y)
        v_set_list[y].discard(d)
      if l > -1:
        h_set_list[x].discard(l)
        v_set_list[l].discard(x)
      if r < W:
        h_set_list[x].discard(r)
        v_set_list[r].discard(x)

  ans = 0
  for i in range(H):
    ans += len(h_set_list[i]) - 2

  print(ans)



if __name__ == "__main__":
  main()