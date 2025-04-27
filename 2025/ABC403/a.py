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
  a_list = list(map(int, input().split()))

  ans = 0

  for i in range(n):
    if not i%2:
      ans += a_list[i]

  print(ans)

if __name__ == "__main__":
  main()