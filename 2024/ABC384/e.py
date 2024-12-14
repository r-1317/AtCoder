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
  h, w, b = map(int, input().split())
  p, q = map(int, input().split())
  grid = [[None] * (w+2) for _ in range(h+2)]

  for i in range(1, h+1):
    tmp_list = list(map(int, input().split()))
    for j in range(1, w+1):
      grid[i][j] = tmp_list[j-1]

  power = grid[p][q]
  grid[p][q] = None
  ic(power)

  adj_list = [[0, 1], [0, -1], [1, 0], [-1, 0]]

  neighbor_list = []

  for adj in adj_list:
    x, y = adj
    s = grid[p+x][q+y]
    if s is not None:
      neighbor_list.append([s, p+x, q+y])
      grid[p+x][q+y] = None
      neighbor_list.sort()

  ic(neighbor_list)

  while neighbor_list[0][0]*b < power:
    s, x, y = neighbor_list.pop(0)
    ic(s, x, y)
    power += s
    for adj in adj_list:
      dx, dy = adj
      s = grid[x+dx][y+dy]
      ic(s)
      if s is not None:
        # neighbor_list.append([s, x+dx, y+dy])
        neighbor_list.insert(bisect.bisect(neighbor_list, [s, x+dx, y+dy]), [s, x+dx, y+dy])
        grid[x+dx][y+dy] = None
    # neighbor_list.sort(key=lambda x: x[0])
    if not neighbor_list:
      break
    ic(neighbor_list)
    ic(grid)

  ic(grid)

  print(power)


if __name__ == "__main__":
  main()