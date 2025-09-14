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
  N, R = map(int, input().split())
  l_list = list(map(int, input().split()))

  left = 10**9
  for i in range(N):
    if not l_list[i]:
      left = i
      break

  right = -10**9
  for i in range(N-1, -1, -1):
    if not l_list[i]:
      right = i+1
      break

  left = min(left, R)
  right = max(right, R)

  ans = right - left

  ans += sum(l_list[left:right])

  print(ans)

if __name__ == "__main__":
  main()