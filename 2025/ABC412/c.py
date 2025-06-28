import os
import bisect

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  t = int(input())

  for _ in range(t):
    n = int(input())
    s_list = list(map(int, input().split()))
    first = s_list[0]
    last = s_list[-1]
    s_list = s_list[1:-1]
    s_list.sort()
    s_list = [first] + s_list + [last]
    ic(n, s_list, first, last)
    domino_list = [first]
    flag = True
    current_domino_index = 0
    next_domino = 0

    while domino_list[-1]*2 < last:
      for i in range(current_domino_index + 1, n):
        if domino_list[-1]*2 < s_list[i]:
          ic(s_list[i], domino_list[-1]*2)
          next_domino = i - 1
          break
        elif i == n - 1:
          next_domino = i
      if current_domino_index == next_domino:
        flag = False
        break
      ic(next_domino)
      domino_list.append(s_list[next_domino])
      current_domino_index = next_domino
    ic(domino_list)

    if flag:
      ans = len(domino_list) + 1
    else:
      ans = -1
    ic(ans)
    print(ans)

if __name__ == "__main__":
  main()