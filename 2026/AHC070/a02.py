import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

MOVES = [(10, 1), (4, 0), (1, 1)]
N = 100
M = 3

def main():
  for move in MOVES:
    print(move[0], move[1])
  pos = [0, 0]
  for i in range(10000):
    if i % 2500 == 0:
      m = 2
    elif i % 100 == 0:
      m = 1
    else:
      m = 0
    pos[0] = (pos[0] + MOVES[m][0]) % N
    pos[1] = (pos[1] + MOVES[m][1]) % N
    print(m)


if __name__ == "__main__":
  main()