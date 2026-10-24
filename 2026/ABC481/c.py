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

  d = dict()
  next_id = 1

  for _ in range(Q):
    s = input()
    if s not in d:
      d[s] = next_id
      next_id += 1
    print(d[s])


if __name__ == "__main__":
  main()