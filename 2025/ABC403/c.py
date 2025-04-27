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
  n, m, q = map(int, input().split())

  premission_set_list = [set() for _ in range(n)]
  all_permission_list = [False] * n

  for i in range(q):
    query = list(map(int, input().split()))
    if query[0] == 1:
      x, y = query[1] - 1, query[2] - 1
      premission_set_list[x].add(y)
    elif query[0] == 2:
      x = query[1] - 1
      all_permission_list[x] = True
    elif query[0] == 3:
      x, y = query[1] - 1, query[2] - 1
      ans = y in premission_set_list[x] or all_permission_list[x]
      if ans:
        print("Yes")
      else:
        print("No")

if __name__ == "__main__":
  main()