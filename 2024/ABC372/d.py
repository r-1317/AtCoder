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
  h_list = list(map(int, input().split()))
  ans_list = [0]*n

  for i in range(n):
    max = 0
    ans = 0
    for j in range(i+1, n):
      if max < h_list[j]:
        ans += 1
        max = h_list[j]
    ans_list[i] = ans

  print(*ans_list)

if __name__ == "__main__":
  main()