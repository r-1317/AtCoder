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
  H, W, Q = map(int, input().split())

  chocolate = [H, W]

  for _ in range(Q):
    query = list(map(int, input().split()))

    if query[0] == 1:
      r = query[1]
      ic(chocolate[1]*r)
      print(chocolate[1]*r)
      chocolate[0] -= r
    else:
      c = query[1]
      ic(chocolate[0]*c)
      print(chocolate[0]*c)
      chocolate[1] -= c


if __name__ == "__main__":
  main()