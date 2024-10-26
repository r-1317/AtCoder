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
  n, m = map(int, input().split())
  l_r_list = [tuple(map(int, input().split())) for _ in range(n)]

  l_r_list.sort(key=lambda x: x[0])
  l_r_list.append((10**9, 10**9))

  min_r_list = [0]*(m+1)
  min_r = m+1
  index = 0

  for i in range(n):
    l, r = l_r_list[i]
    min_r_list[l] = r

  

if __name__ == "__main__":
  main()