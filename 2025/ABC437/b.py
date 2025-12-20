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
  H, W, N = map(int, input().split())

  a_list = [list(map(int, input().split())) for _ in range(H)]

  b_list = [int(input()) for _ in range(N)]

  point_list = [0]*H

  for b in b_list:
    for i in range(H):
      if b in a_list[i]:
        point_list[i] += 1

  print(max(point_list))

if __name__ == "__main__":
  main()