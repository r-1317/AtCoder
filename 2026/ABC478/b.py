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
  N, V = map(int, input().split())
  w_list = list(map(int, input().split()))

  ans = 0
  for i in range(N - 2):
    for j in range(i + 1, N - 1):
      for k in range(j + 1, N):
        if k == i or k == j:
          continue
        if i + j + k > V - 3:
          continue
        ans = max(ans, w_list[i] + w_list[j] + w_list[k])

  print(ans)

if __name__ == "__main__":
  main()