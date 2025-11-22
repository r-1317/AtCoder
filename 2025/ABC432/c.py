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
  N, X, Y = map(int, input().split())
  a_list = list(map(int, input().split()))
  diff = Y - X

  all_y_list = [0]*N
  for i in range(N):
    all_y_list[i] = a_list[i] * Y
  
  min_all_y = min(all_y_list)
  ic(min_all_y)

  count = 0
  vaild = True
  for i in range(N):
    da = all_y_list[i] - min_all_y
    if da % diff != 0:
      vaild = False
      break
    if da // diff > a_list[i]:  # 疑惑
      vaild = False
      break
    count += da // diff
  
  if not vaild:
    ans = -1
  else:
    ans = sum(a_list) - count

  print(ans)

if __name__ == "__main__":
  main()