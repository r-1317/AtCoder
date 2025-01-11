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
  n, d = map(int, input().split())
  t_l_list = [list(map(int, input().split())) for _ in range(n)]

  for i in range(1, d+1):
    max_w = 0
    for t, l in t_l_list:
      max_w = max(max_w, t * (l+i))
    print(max_w)

if __name__ == "__main__":
  main()