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

  x_l_r_list = []
  for _ in range(Q):
    l, r, x = map(int, input().split())
    l -= 1
    r -= 1
    x_l_r_list.append([x, l, r])

  x_l_r_list.sort()
  x_l_r_list.append([10**9, N + 1, N + 1])

  imos_list = [0]*(N + 3)
  current_x = -1
  min_l = N + 1
  max_r = N + 1
  for x, l, r in x_l_r_list:
    ic(x, l, r)
    if x != current_x:
      if min_l != -1:
        imos_list[min_l] += 1
        imos_list[max_r + 1] -= 1
        ic(min_l, max_r + 1, x)
      min_l = l
      max_r = r
      current_x = x
    if min_l == -1:
      min_l = l
      max_r = r
    if l > max_r + 1:  # 精算
      imos_list[min_l] += 1
      imos_list[max_r + 1] -= 1
      ic(min_l, max_r + 1, x, "a")
      min_l = l
      max_r = r
    else:
      max_r = max(max_r, r)

  ans_list = [imos_list[0]]
  for i in range(1, N):
    ans = ans_list[-1] + imos_list[i]
    ans_list.append(ans)

  ic(imos_list)
  print(*ans_list[:N])

if __name__ == "__main__":
  main()