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
  N, D = map(int, input().split())
  x_list = list(map(int, input().split()))

  ans_list = []
  for i in range(N):
    x = x_list[i]
    flag = True
    for j in range(N):
      if i == j:
        continue
      y = x_list[j]
      if abs(x - y) < D:
        flag = False
    if flag:
      ans_list.append(i + 1)

  print(len(ans_list))
  print(*ans_list)

if __name__ == "__main__":
  main()