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
  N, M = map(int, input().split())

  ans = 0
  for i in range(61):
    if not (M >> i & 1):
      continue
    

if __name__ == "__main__":
  main()