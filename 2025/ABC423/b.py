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
  l_list = list(map(int, input().split()))

  ans = N - 1

  count = 0
  for i in range(N):
    if l_list[i] == 0:
      count += 1
    else:
      break
  
  for i in range(N-1, -1, -1):
    if l_list[i] == 0:
      count += 1
    else:
      break

  ans = max(0, ans - count)

  print(ans)

if __name__ == "__main__":
  main()