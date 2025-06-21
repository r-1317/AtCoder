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
  n, s = map(int, input().split())
  t_list = list(map(int, input().split()))

  tmp = 0

  flag = True

  for i in range(n):
    if (t_list[i] - tmp) > s:
      flag = False
      break
    tmp = t_list[i]

  print("Yes" if flag else "No")

if __name__ == "__main__":
  main()