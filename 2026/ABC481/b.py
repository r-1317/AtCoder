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

  ans = 0
  for a in a_list:
    if a == K:
      ans += 1
  for i in range(N - 1):
    if min(a_list[i], a_list[i+1]) < K < max(a_list[i], a_list[i+1]):
      ans += 1

  print(ans)

if __name__ == "__main__":
  main()