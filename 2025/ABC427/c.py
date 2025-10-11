import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

# ic.enable() if MyPC else None

def main():
  N, M = map(int, input().split())
  edge_list = [list(map(int, input().split())) for _ in range(M)]

  min_cost = 10**9

  for i in range(2**N):
    ic(i)
    str_i = format(i, '01200b')
    list_i = list(str_i)
    # str_i.reverse()
    # list_i = reversed(list_i)
    ic(str_i)
    cost = 0
    for u, v in edge_list:
      # u -= 1
      # v -= 1

      ic(u, v)

      if list_i[-u] == list_i[-v]:
        cost += 1
      else:
        ic(list_i[-u], list_i[-v])

    min_cost = min(min_cost, cost)
    # print(min_cost)
    ic(cost)

  print(min_cost)


if __name__ == "__main__":
  main()