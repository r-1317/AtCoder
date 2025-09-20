import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def is_2x2(grid, h, w):
  H = len(grid)
  W = len(grid[0])
  if grid[h][w] == "#" and grid[h+1][w] == "#" and grid[h][w+1] == "#" and grid[h+1][w+1] == "#":
    return True
  return False

def main():
  T = int(input())

  for _ in range(T):
    H, W = map(int, input().split())
    grid = [input() for _ in range(H)]
    erase_point_list = [[0]*W for _ in range(H)]
    erase_src_set = [[set() for _ in range(W)] for _ in range(H)]  # 右上の座標を格納

    for h in range(H-1):
      for w in range(W-1):
        if is_2x2(grid, h, w):
          erase_point_list[h][w] += 1
          erase_point_list[h+1][w] += 1
          erase_point_list[h][w+1] += 1
          erase_point_list[h+1][w+1] += 1
          erase_src_set[h][w].add((h, w))
          erase_src_set[h+1][w].add((h, w))
          erase_src_set[h][w+1].add((h, w))
          erase_src_set[h+1][w+1].add((h, w))

    # cell_sorted_by_erase_point = [(h, w) for h in range(H) for w in range(W)]
    # cell_sorted_by_erase_point.sort(key=lambda x: erase_point_list[x[0]][x[1]], reverse=True)

    ans = 0

    while True:
      # erase_pointが1のセルを探す
      e1_coord = (-1, -1)
      for h in range(H):
        for w in range(W):
          if erase_point_list[h][w] == 1:
            e1_coord = (h, w)
            break

      if e1_coord == (-1, -1):
        break

      ans += 1
      eh, ew = e1_coord
      e_coord_list = list(erase_src_set[eh][ew])
      for eh, ew in e_coord_list:
        erase_point_list[eh][ew] -= 1
        erase_point_list[eh+1][ew] -= 1
        erase_point_list[eh][ew+1] -= 1
        erase_point_list[eh+1][ew+1] -= 1

        erase_src_set[eh][ew].remove((eh, ew))
        erase_src_set[eh+1][ew].remove((eh, ew))
        erase_src_set[eh][ew+1].remove((eh, ew))
        erase_src_set[eh+1][ew+1].remove((eh, ew))


      # h, w = cell_sorted_by_erase_point[0]
      # if erase_point_list[h][w] == 0:
      #   continue

      # ans += 1
      # e_coord_list = list(erase_src_set[h][w])
      # for eh, ew in e_coord_list:
      #   erase_point_list[eh][ew] -= 1
      #   erase_point_list[eh+1][ew] -= 1
      #   erase_point_list[eh][ew+1] -= 1
      #   erase_point_list[eh+1][ew+1] -= 1

      #   erase_src_set[eh][ew].remove((eh, ew))
      #   erase_src_set[eh+1][ew].remove((eh, ew))
      #   erase_src_set[eh][ew+1].remove((eh, ew))
      #   erase_src_set[eh+1][ew+1].remove((eh, ew))

      # cell_sorted_by_erase_point.sort(key=lambda x: erase_point_list[x[0]][x[1]], reverse=True)

    print(ans)

if __name__ == "__main__":
  main()