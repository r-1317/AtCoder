import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def move(i, j, s_list, k, prev_list):
  if s_list[i][j] == "#":
    return 0

  if len(prev_list) == k:
    return 1

  ans = 0
  for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
    next_i = i + dx
    next_j = j + dy
    if not (next_i, next_j) in prev_list:
      ans += move(next_i, next_j, s_list, k, prev_list + [(i, j)])

  return ans

def main():
  h, w, k = map(int, input().split())
  # s_listの周囲を#で囲む
  s_list = [["#"] + list(input()) + ["#"] for _ in range(h)]
  s_list = [["#"]*(w+2)] + s_list + [["#"]*(w+2)]
  ic(s_list)

  ans = 0

  for i in range(1,h+1):
    for j in range(1,w+1):
      ans += move(i, j, s_list, k, [])

  print(ans)



if __name__ == "__main__":
  main()