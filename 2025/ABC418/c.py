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
  N, Q = map(int, input().split())
  a_list = list(map(int, input().split()))

  a_imos_list = [0]*(10**6 + 2)
  for i in range(N):
    a_imos_list[a_list[i]] += 1

  a_cost_list = [-1]*(10**6 + 2)
  a_cost_list[0] = 0
  current_cost = N
  for i in range(1, 10**6 + 2):
    a_cost_list[i] = a_cost_list[i-1] + current_cost
    current_cost -= a_imos_list[i]
    if current_cost <= 0:
      break

  for _ in range(Q):
    B = int(input())
    if a_cost_list[B] == -1:
      ans = -1
    else:
      ans = a_cost_list[B-1]+1
    ic(ans)
    print(ans)


if __name__ == "__main__":
  main()