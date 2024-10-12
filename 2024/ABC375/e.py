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
  n = int(input())
  team_list = [[] for _ in range(3)]
  sum_list = [0]*3

  for i in range(n):
    a, b = map(int, input().split())
    team_list[a-1].append(b)

if __name__ == "__main__":
  main()