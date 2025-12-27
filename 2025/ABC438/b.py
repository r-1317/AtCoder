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
  N, M = map(int, input().split())
  S = list(map(int, list(input())))
  T = list(map(int, list(input())))

  ic(S)
  ic(T)

  min_cost = 10**9

  for i in range(N - M + 1):
    ic(i)
    cost = 0
    for j in range(M):
      cost += (S[i+j] - T[j]) % 10
    min_cost = min(min_cost, cost)

  print(min_cost)

if __name__ == "__main__":
  main()