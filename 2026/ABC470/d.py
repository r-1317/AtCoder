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
  p_list = [0] + list(map(int, input().split()))

  idx_list = [-1]*(N+1)
  for i in range(N+1):
    idx_list[p_list[i]] = i

  ic(p_list)
  ic(idx_list)

  for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 1:
      x, y = query[1], query[2]
      idx_list[p_list[x]], idx_list[p_list[y]] = idx_list[p_list[y]], idx_list[p_list[x]]
      p_list[x], p_list[y] = p_list[y], p_list[x]
    if query[0] == 2:
      p_list, idx_list = idx_list, p_list
    # ic(p_list)
    # ic(idx_list)

  print(*p_list[1:])


if __name__ == "__main__":
  main()