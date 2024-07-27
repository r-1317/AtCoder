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
  h, w = map(int, input().split())
  tmp_coord = list(map(int, input().split()))

  tmp_coord[0] -= 1
  tmp_coord[1] -= 1

  map_list = [list(input()) for _ in range(h)]

  x = input()  # L, R, U, Dからなる文字列

  for i in range(len(x)):
    if x[i] == "L" and 0 < tmp_coord[1]:
      if map_list[tmp_coord[0]][tmp_coord[1]-1] == ".":
        tmp_coord[1] -= 1

    elif x[i] == "R" and tmp_coord[1] < w-1:
      if map_list[tmp_coord[0]][tmp_coord[1]+1] == ".":
        tmp_coord[1] += 1

    elif x[i] == "U" and 0 < tmp_coord[0]:
      if map_list[tmp_coord[0]-1][tmp_coord[1]] == ".":
        tmp_coord[0] -= 1

    elif x[i] == "D" and tmp_coord[0] < h-1:
      if map_list[tmp_coord[0]+1][tmp_coord[1]] == ".":
        tmp_coord[0] += 1

    ic(tmp_coord)

  tmp_coord[0] += 1
  tmp_coord[1] += 1

  print(*tmp_coord)



if __name__ == "__main__":
  main()