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
  n = int(input())
  
  ans = 0
  prev_t = 0

  for i in range(n):
    t, v = map(int, input().split())
    ans = max(ans - (t - prev_t), 0)
    ans += v
    prev_t = t
  
  print(ans)

if __name__ == "__main__":
  main()