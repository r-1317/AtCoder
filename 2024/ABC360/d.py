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
  n, t = map(int, input().split())  # n: 蟻の数, t: 移動時間
  s = input() # 蟻の方向
  x_list = list(map(int, input().split())) # 蟻の初期位置

  # 蟻の速度は一定であるため、t秒後には初期位置からtだけ進む。

  # 蟻の位置を正負で分ける
  left = [0]*n
  right = [0]*n

  left_tmp = 0
  right_tmp = 0

  for i in range(n):
    if s[i] == "0":
      left[left_tmp] = x_list[i]
      left_tmp += 1
    else: 
      right[right_tmp] = x_list[i]
      right_tmp += 1

  left = left[:left_tmp]
  right = right[:right_tmp]

  # ic(left)
  # ic(right)

  # 蟻の位置をソート
  left.sort()
  right.sort()

  ic(left)
  ic(right)

  left_dist = [0]*len(left)
  right_dist = [0]*len(right)

  for i in range(len(left)):
    left_dist[i] = left[i] - t

  for i in range(len(right)):
    right_dist[i] = right[i] + t

  ic(left_dist)
  ic(right_dist)

  # 蟻どうしがすれ違うかどうか
  ans = 0
  # 二分探索により、すれ違うかどうかを判定する
  # すれ違う条件は、left_dist[i] <= right_dist[j] かつ left[i] >= right_dist[j] である。

  for i in range(len(left)):
    start = left[i]  # 開始位置
    dist = left_dist[i]  # 終了位置

    # 開始位置が自分より左にいる蟻のindexを探す
    left_index = 0
    right_index = len(right)-1

    while left_index < right_index:
      mid = (left_index + right_index) // 2
      if right[mid] < start:
        left_index = mid + 1
      else:
        right_index = mid
    ic(left_index, mid, right_index)

    min = mid

    # 二分探索がうまく行かないので微調整
    if right[0] > start:
      min = -1
    else:
      while min+1 < len(right):
        if right[min+1] < start:
          min += 1
        else:
          break

    ic(min)

    # 終了位置が自分より右にいる蟻のindexを探す
    left_index = 0
    right_index = len(right_dist)-1

    while left_index < right_index:
      mid = (left_index + right_index) // 2
      if right_dist[mid] < dist:
        left_index = mid + 1
      else:
        right_index = mid
    ic(left_index, mid, right_index)

    max = mid

    # 二分探索がうまく行かないので微調整
    if right_dist[-1] < dist:
      max = len(right_dist)
    else:
      while max-1 >= 0:
        if right_dist[max-1] < dist:
          break
        else:
          max -= 1

    ic(max)




if __name__ == "__main__":
  main()