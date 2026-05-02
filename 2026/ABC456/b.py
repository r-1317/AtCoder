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
  a_list = [list(map(int, input().split())) for _ in range(3)]

  count = 0

  for i in range(6):
    for j in range(6):
      for k in range(6):
        if sorted([a_list[0][i], a_list[1][j], a_list[2][k]]) == [4, 5, 6]:
          count += 1
          ic(sorted([i, j, k]))
  
  print(count / 6**3)

if __name__ == "__main__":
  main()