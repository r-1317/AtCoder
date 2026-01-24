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

  cum_sum_list = [0]

  for i in range(N):
    cum_sum_list.append(cum_sum_list[-1] + a_list[i])

  for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 1:
      x = query[1]-1
      a_list[x], a_list[x+1] = a_list[x+1], a_list[x]
      cum_sum_list[x+1] += a_list[x] - a_list[x+1]
    elif query[0] == 2:
      # ic(a_list)
      # ic(cum_sum_list)
      l, r = query[1], query[2]
      # ic(cum_sum_list[r] - cum_sum_list[l-1])
      print(cum_sum_list[r] - cum_sum_list[l-1])


if __name__ == "__main__":
  main()