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
  H, W = map(int, input().split())

  for i in range(H):
    flag1 = False
    if i == 0 or i == H-1:
      flag1 = True
    for j in range(W):
      if j == 0 or j == W-1 or flag1:
        flag = True
      else:
        flag = False
      print("#" if flag else ".", end="")
    print()  # 改行

if __name__ == "__main__":
  main()