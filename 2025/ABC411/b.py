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
  d_list = list(map(int, input().split()))

  for i in range(n - 1):
    for j in range(i, n-1):
      ans = sum(d_list[i:j + 1])
      print(ans, end=" ")
    print()

if __name__ == "__main__":
  main()