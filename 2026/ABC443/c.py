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
  N, T = map(int, input().split())
  a_list = list(map(int, input().split()))

  ans = 0
  next_open = 0

  for a in a_list:
    if next_open > a:
      continue
    ic(a, next_open)
    ans += a - next_open
    next_open = a + 100
  
  ans += max(0, T - next_open)

  print(ans)

if __name__ == "__main__":
  main()