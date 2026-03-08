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
  c_list = list(map(int, input().split()))

  ans = 0

  for _ in range(N):
    a, b = map(int, input().split())
    a -= 1

    d = min(c_list[a], b)
    c_list[a] -= d
    ans += d

  print(ans)

if __name__ == "__main__":
  main()