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

  bag = []

  for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 1:
      bag.append(query[1])
      bag.sort()
    elif query[0] == 2:
      ans = bag.pop(0)
      ic(ans)
      print(ans)

if __name__ == "__main__":
  main()