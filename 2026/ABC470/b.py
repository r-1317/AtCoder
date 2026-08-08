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
  c_list = list(map(int, input().split()))

  count = 0

  for i in range(1, N+1):
    count = max(count, c_list.count(i))

  print(N - count)

if __name__ == "__main__":
  main()