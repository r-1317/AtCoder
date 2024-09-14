import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# 二分探索で、l以上r以下の範囲のindexを取得する
def find_index(x_list, l, r):
  mid = len(x_list) // 2
  x = mid//2

  while 0 < x:
    if x_list[mid] < l:
      mid += x
    else:
      mid -= x
    x = x // 2

  l_index = mid

  mid = len(x_list) // 2
  x = mid//2

  while 0 < x:
    if x_list[mid] < r:
      mid += x
    else:
      mid -= x
    x = x // 2

  r_index = mid

  ic(l_index, r_index)
  ic("微調整後")

  if x_list[-1] < l or r < x_list[0]:
    return None, None

  # 微調整
  while True:
    if x_list[l_index] < l:
      l_index += 1
    
    if l_index != 0:
      if l <= x_list[l_index-1]:
        l_index -= 1

    if l_index == 0:
      break
    elif x_list[l_index-1] < l and l <= x_list[l_index]:
      break

  while True:
    if r < x_list[r_index]:
      r_index -= 1
    
    if r_index != len(x_list) - 1:
      if x_list[r_index+1] <= r:
        r_index += 1

    ic(r_index, len(x_list))
    if r_index == len(x_list) - 1:
      break
    elif x_list[r_index] <= r and r < x_list[r_index+1]:
      break

  return l_index, r_index


def main():
  n = int(input())
  x_list = list(map(int, input().split()))  # 村の座標(1次元)
  p_list = list(map(int, input().split()))  # 村の人口

  p_sum_list = [0] * (n+1)  # 村iまでの人口の合計
  p_sum_list[0] = 0
  for i in range(1, n+1):
    p_sum_list[i] = p_sum_list[i - 1] + p_list[i-1]

  ic(p_sum_list)

  q = int(input())  # クエリ数
  for _ in range(q):
    l, r = map(int, input().split())  # 座標の範囲
    ic(l, r)

    l_index, r_index = find_index(x_list, l, r)
    ic(l_index, r_index)
    if l_index is None:
      print(0)
      continue
    ic(p_sum_list[l_index], p_sum_list[r_index+1])

    ans = p_sum_list[r_index+1] - p_sum_list[l_index]

    print(ans)

if __name__ == "__main__":
  main()