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
  N = int(input())
  a_list = [N+1] + list(map(int, input().split()))

  count_list = [0]*(N+2)
  max_len = 0
  l = 1

  for i in range(1, N + 1):
    count_list[a_list[i]] += 1
    if count_list[a_list[i]] > 2:  # 同じ数が3つ以上出てきたら2つになるまで削る
      ic(i, a_list[l: i+1])
      while count_list[a_list[i]] > 2:
        count_list[a_list[l]] -= 1
        l += 1
      if l < i and a_list[l] != a_list[l+1]:  # ズレている場合の対処になると思う
        count_list[a_list[l]] -= 1
        l += 1
      ic(a_list[l: i+1])
    if (i - l + 1) % 2:  # 奇数なら何もせず通過
      continue
    if a_list[i] != a_list[i-1]:  # 直前の数と違いが生じたらそこまで削る
      while l < i:
        count_list[a_list[l]] -= 1
        l += 1

    if (i - l + 1) % 2 == 0:
      max_len = max(max_len, i - l + 1)
      # ic((i - l + 1) % 2)

  print(max_len)

if __name__ == "__main__":
  main()