import os

if os.path.basename(__file__) != "Main.py":
  from icecream import ic
else:
  def ic(*args):
    return None

# ic.disable() if os.path.basename(__file__) != "Main.py" else None

def main():
  a, b, c, d, e, f = map(int, input().split())  # a:1円, b:5円, c:10円, d:50円, e:100円, f:500円
  n = int(input())
  x_list = list(map(int, input().split()))
  # x_list.sort()
  flag = True

  for x in x_list:

    ic(x, a, b, c, d, e, f)

    while 500 <= x:
      if 0 < f:
        x -= 500
        f -= 1
      else:
        break

    ic(x, a, b, c, d, e, f)

    while 100 <= x:
      if 0 < e:
        x -= 100
        e -= 1
      else:
        break

    ic(100 < x)
    ic(x, a, b, c, d, e, f)

    while 50 <= x:
      if 0 < d:
        x -= 50
        d -= 1
      else:
        break

    ic(x, a, b, c, d, e, f)

    while 10 <= x:
      if 0 < c:
        x -= 10
        c -= 1
      else:
        break

    ic(x, a, b, c, d, e, f)

    while 5 <= x:
      if 0 < b:
        x -= 5
        b -= 1
      else:
        break

    ic(x, a, b, c, d, e, f)

    if x <= a:
      a -= x
    else:
      flag = False
      break

  print("Yes" if flag else "No")


if __name__ == "__main__":
  main()