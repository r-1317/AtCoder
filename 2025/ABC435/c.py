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

  ans = 0

  max_t = 1

  for i in range(N):
    if i < max_t:
      ans = i
      max_t = max(max_t, i + a_list[i])

  print(ans+1)

if __name__ == "__main__":
  main()