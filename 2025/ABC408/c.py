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
  l_r_list = [list(map(int, input().split())) for _ in range(m)]

  imos_list = [0] * (n + 1)

  for l, r in l_r_list:
    imos_list[l - 1] += 1
    imos_list[r] -= 1

  tmp = 0
  min_value = float('inf')

  for i in range(n):
    tmp += imos_list[i]
    if tmp < min_value:
      min_value = tmp

  print(min_value)

if __name__ == "__main__":
  main()