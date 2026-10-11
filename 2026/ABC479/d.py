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
  N, Q = map(int, input().split())
  l_list = [10**18] + list(map(int, input().split()))
  r_list = list(map(int, input().split())) + [10**18]
  lowest_r_list = [10**18]*N  # 右に行くときに一旦左を経由するときと合わせた最小コスト
  lowest_l_list = [10**18]*N

  min_r = 10**18
  for i in range(N):
    lowest_r = min(l_list[i] + min_r, r_list[i])
    lowest_r_list[i] = lowest_r
    min_r = min(min_r, r_list[i])

  min_l = 10**18
  for i in range(N - 1, -1, -1):
    lowest_l = min(r_list[i] + min_l, l_list[i])
    lowest_l_list[i] = lowest_l
    min_l = min(min_l, l_list[i])

  for _ in range(Q):
    s, t = map(int, input().split())
    s -= 1
    t -= 1
    if s < t:
      ans = lowest_r_list[s]
    else:
      ans = lowest_l_list[s]
    ic(ans)
    print(ans)


if __name__ == "__main__":
  main()