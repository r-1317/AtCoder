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
  N, M, K = map(int, input().split())
  a_list = list(map(int, input().split()))

  a_list = [0]*M + a_list
  visited_list = [False]*(N+M)
  current = 0  # 直近M日間のカロリー

  for i in range(M, N+M):
    if visited_list[i - M]:
      current -= a_list[i - M]

    if current + a_list[i] <= K:
      current += a_list[i]
      visited_list[i] = True
      print("Yes")
    else:
      print("No")

if __name__ == "__main__":
  main()