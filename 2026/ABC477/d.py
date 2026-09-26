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
  ic()
  N, Q = list(map(int, input().split()))

  tile_time_list = [1000000.0]*N
  tile_list = [False]*N
  c_list = [(-1.0, "a")]  # (時刻, 色)
  new_open_set = set()
  new_close_set = set()
  for i in range(Q):
    queue = list(input().split())
    if queue[0] == "1":
      x = int(queue[1])
      x -= 1
      if x in new_open_set:
        new_open_set.discard(x)
      elif x in new_close_set:
        new_close_set.discard(x)
      else:
        if tile_list[x]:
          new_open_set.add(x)
        else:
          new_close_set.add(x)
    elif queue[0] == "2":
      c = queue[1]
      for y in new_close_set:
        tile_time_list[y] = i - 0.5
        tile_list[y] = True
      for y in new_open_set:
        tile_time_list[y] = 1000000.0
        tile_list[y] = False
      c_list.append((float(i), c))
      new_open_set = set()
      new_close_set = set()

  ic()

  ans = ""
  for i in range(N):
    c_idx = bisect.bisect(c_list, (tile_time_list[i], "x")) - 1
    c = c_list[c_idx][1]
    ans += c

  print(ans)
  ic()


if __name__ == "__main__":
  main()