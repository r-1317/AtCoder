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
  Q = int(input())

  t_list = []
  debt = 0
  closing_idx_list = []

  for _ in range(Q):
    query = list(input().split())
    if query[0] == "1":
      c = query[1]
      t_list.append(c)

      if c == "(":
        debt += 1
      elif c == ")":
        debt -= 1
        if debt < 0:
          closing_idx_list.append(len(t_list)-1)
    
    elif query[0] == "2":
      c = t_list.pop()
      if c == "(":
        debt -= 1
      elif c == ")":
        debt += 1
      if closing_idx_list and closing_idx_list[-1] == len(t_list):
        closing_idx_list.pop()

    ans = not(debt or closing_idx_list)

    # ic(debt)
    # ic(t_list)
    # ic(closing_idx_list)
    # ic(ans)
    print("Yes" if ans else "No")



if __name__ == "__main__":
  main()