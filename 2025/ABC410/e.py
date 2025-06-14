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
  n, h, m = map(int, input().split())
  a_b_list = [list(map(int, input().split())) for _ in range(n)]

  dp_list = [[m] * (h + 1) for _ in range(n + 1)]

  ans = n

  for i in range(1, n + 1):
    a, b = a_b_list[i - 1]
    for j in range(h + 1):
      dp_list[i][j] = dp_list[i - 1][j] - b
      if a <= j:
        dp_list[i][j - a] = max(dp_list[i - 1][j], dp_list[i][j - a])
    
    flag = False
    for j in range(h + 1):
      if 0 <= dp_list[i][j]:
        flag = True
    
    if not flag:
      ans = i - 1
      break

  print(ans)

  # ic(dp_list)

if __name__ == "__main__":
  main()