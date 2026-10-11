import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def dfs(N, W, a_b_list, w, d, i):
  if i == N:
    if w <= W:
      return d
    else:
      return -1

  ans = -1
  ans = max(ans, dfs(N, W, a_b_list, w, d, i + 1))
  new_d = d + a_b_list[i][0]
  new_w = w + a_b_list[i][1]
  ans = max(ans, dfs(N, W, a_b_list, new_w, new_d, i + 1))

  return ans

def main():
  N, W = map(int, input().split())
  a_b_list = [list(map(int, input().split())) for _ in range(N)]

  ans = dfs(N, W, a_b_list, 0, 0, 0)

  print(ans)

if __name__ == "__main__":
  main()