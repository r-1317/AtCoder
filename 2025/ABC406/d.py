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
  h, w, n = map(int, input().split())
  garbage_list = [list(map(int, input().split())) for _ in range(n)]
  x_set_list = [set() for _ in range(h+1)]  # x軸が同じものをまとめる
  y_set_list = [set() for _ in range(w+1)]  # y軸が同じものをまとめる
  x_count_list = [0] * (h+1)  # x軸の数をカウント
  y_count_list = [0] * (w+1)  # y軸の数をカウント
  for x, y in garbage_list:
    x_set_list[x].add(y)
    y_set_list[y].add(x)
    x_count_list[x] += 1
    y_count_list[y] += 1
  
  q = int(input())
  for _ in range(q):
    query = list(map(int, input().split()))
    if query[0] == 1:
      x = query[1]
      ic(x_count_list[x])
      print(x_count_list[x])
      for y in x_set_list[x]:  # 計算量が不明
        y_count_list[y] -= 1
        y_set_list[y].remove(x)
      x_count_list[x] = 0
      x_set_list[x] = set()
    elif query[0] == 2:
      y = query[1]
      ic(y_count_list[y])
      print(y_count_list[y])
      for x in y_set_list[y]:  # 計算量が不明
        x_count_list[x] -= 1
        x_set_list[x].remove(y)
      y_count_list[y] = 0
      y_set_list[y] = set()

if __name__ == "__main__":
  main()