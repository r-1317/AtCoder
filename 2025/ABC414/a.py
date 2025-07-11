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
  N, L, R = map(int, input().split())
  ans = 0
  for i in range(N):
    x, y = map(int, input().split())
    if x <= L and R <= y:
      ans += 1

  print(ans)

if __name__ == "__main__":
  main()