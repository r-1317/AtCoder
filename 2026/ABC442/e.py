import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

class Monster:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def __lt__(self, other):
    pass

def main():
  N, Q = map(int, input().split())
  

if __name__ == "__main__":
  main()