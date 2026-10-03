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
  N, K = map(int, input().split())
  a_list = list(map(int, input().split()))

  x_list = sorted(a_list)
  l = 10**9
  r = -1
  for i in range(N):
    if a_list[i] != x_list[i]:
      if l == 10**9:
        l = i
      r = i

  ic(l, r)

  if r - l <= K - 1:
    print("Yes")
  else:
    print("No")

if __name__ == "__main__":
  main()