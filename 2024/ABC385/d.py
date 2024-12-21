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
  n, m, s_x, s_y = map(int, input().split())
  x_house_dict = {}
  y_house_dict = {}

  for i in range(n):
    x, y = map(int, input().split())
    if x in x_house_dict:
      x_house_dict[x].append(y)
    else:
      x_house_dict[x] = [y]
    if y in y_house_dict:
      y_house_dict[y].append(x)
    else:
      y_house_dict[y] = [x]
  
  ans = 0

  ic(x_house_dict)

  for i in range(m):
    d, c = input().split()
    c = int(c)
    if d == "U":
      if s_x in x_house_dict:
        for y in x_house_dict[s_x]:
          if s_y - c <= y <= s_y:
            ans += 1
            x_house_dict[s_x].remove(y)
            y_house_dict[y].remove(s_x)
      s_y -= c
    elif d == "D":
      if s_x in x_house_dict:
        for y in x_house_dict[s_x]:
          if s_y <= y <= s_y + c:
            ans += 1
            x_house_dict[s_x].remove(y)
            y_house_dict[y].remove(s_x)
      s_y += c
    elif d == "R":
      if s_y in y_house_dict:
        for x in y_house_dict[s_y]:
          if s_x <= x <= s_x + c:
            ans += 1
            y_house_dict[s_y].remove(x)
            x_house_dict[x].remove(s_y)
      s_x += c
    elif d == "L":
      if s_y in y_house_dict:
        for x in y_house_dict[s_y]:
          if s_x - c <= x <= s_x:
            ans += 1
            y_house_dict[s_y].remove(x)
            x_house_dict[x].remove(s_y)
      s_x -= c
    ic(i, ans, s_x, s_y)
  print(s_x, s_y, ans)

if __name__ == "__main__":
  main()