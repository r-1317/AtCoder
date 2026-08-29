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
  a_list = list(map(int, input().split()))

  count_list = [0]*101

  for a in a_list:
    count_list[a] += 1

  ans = 0
  for i, c in enumerate(count_list):
    if c % 2:
      ans += i

  print(ans)

if __name__ == "__main__":
  main()