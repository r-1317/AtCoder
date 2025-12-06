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

  for l in range(N-1):
    for r in range(l+1, N):
      a_sum = 0
      for i in range(l, r+1):
        a_sum += a_list[i]
      flag = True
      for i in range(l, r+1):
        if a_sum % a_list[i] == 0:
          flag = False
          break
      ans += int(flag)

  print(ans)

if __name__ == "__main__":
  main()