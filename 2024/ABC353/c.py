from icecream import ic

# 二分探索によって10**8-a_list[i]を超える要素の数を求める
def more_than_100M(a_list, i, n):

  # ic(i, n)

  left = i+1
  right = n+1

  while right - left > 1:
    mid = (left + right) // 2

    if 10**8 - a_list[i] < a_list[mid]:
      right = mid
    else:
      left = mid

  # ic(left, right)

  if n < right:
    if 10**8 - a_list[i] <= a_list[left]:
      return 1
    else:
      return 0

  elif right == n:
    if 10**8 - a_list[i] <= a_list[left]:
      return 2
    elif 10**8 - a_list[i] <= a_list[right]:
      return 1
    else:
      return 0

  else:
    if 10**8 - a_list[i] <= a_list[left]:
      return n - left + 1
    elif 10**8 - a_list[i] <= a_list[right]:
      return n - left
    else:
      return n - left - 1

  # 廃止
  if a_list[-1] < 10**8 - a_list[i]:
    return 0
  elif 10**8 - a_list[i] <= a_list[left]:
    return n - left + 1
  else:
    return n - left

def main():
  n = int(input())
  a_list = [0] + list(map(int, input().split()))  # 要素[0]は無視
  a_list.sort()

  # ic(a_list)

  ans = 0

  # まず (i+j) の総和を求める
  for i in range(1,n+1):
    ans += a_list[i]*(n-1)

  # 次に 10**8 を超える組の数を求める

  count = 0

  for i in range(1,n):
    count += more_than_100M(a_list, i, n)
    # ic(more_than_100M(a_list, i, n))

  # ic(count)

  print(ans - count*10**8)

if __name__ == "__main__":
  main()