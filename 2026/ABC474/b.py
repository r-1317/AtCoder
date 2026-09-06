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
  p_list = map(int, input().split())  # listになっていないけれど偶然問題なく実行できた

  ans = True
  for i, p in enumerate(p_list):
    p -= 1
    if p // 10 != i // 10:
      ans = False
      break

  print("Yes" if ans else "No")

if __name__ == "__main__":
  main()