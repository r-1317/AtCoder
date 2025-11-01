import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def is_valid(grid, H, W, sx, sy, booth_coord_list):

  if not(booth_coord_list[0] != booth_coord_list[1] != booth_coord_list[2]):
    return False
  for x, y in booth_coord_list:
    if grid[x][y] == "#":
      return False
  if (sx, sy) in booth_coord_list:
    return False
  if grid[sx][sy] == "#":
    return False

  visited_grid = [[False]*W for _ in range(H)]

  # bfs
  booth_checked_coount = 0

  # queue = [booth_coord_list[-1]]
  # x, y = queue[-1]
  # visited_grid[x][y] = True

  queue = [(sx, sy)]

  while queue:
    x, y = queue.pop()

    for dx in (-1, 0, 1):
      for dy in (-1, 0, 1):
        if dx and dy:
          continue
        nx = x + dx
        ny = y + dy
        if not((0 <= nx < H) and (0 <= ny < W)):
          continue
        if visited_grid[nx][ny]:
          continue
        if grid[nx][ny] != ".":
          continue
        if (nx, ny) in booth_coord_list:
          booth_checked_coount += 1
          visited_grid[nx][ny] = True
          continue
        queue.append((nx, ny))
        visited_grid[nx][ny] = True

  if booth_checked_coount == 3:
    # ic(booth_coord_list, sx, sy)
    return True
  else:
    return False

def main():
  H, W = map(int, input().split())

  grid = [list(input()) for _ in range(H)]

  ans = 0

  booth_set = set()

  for x1 in range(H):
    for y1 in range(W):
      for x2 in range(H):
        for y2 in range(W):
          for x3 in range(H):
            for y3 in range(W):
              booth_coord_list = [(x1, y1), (x2, y2), (x3, y3)]
              booth_coord_list = sorted(booth_coord_list)
              list_id = x1 + y1*10 **1+ x2 * 10**2 + y2 * 10**3 + x3 * 10**4 + y3 * 10**5
              if list_id in booth_set:
                continue
              flag = False
              for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                  if dx and dy:
                    continue
                  sx = x1 + dx
                  sy = y1 + dy
                  if not((0 <= sx < H) and (0 <= sy < W)):
                    continue
                  flag = is_valid(grid, H, W, sx, sy, booth_coord_list)
                  if flag:
                    break
                if flag:
                  break
              ans += int(flag)
              booth_set.add(list_id)

  print(ans//6)



if __name__ == "__main__":
  main()