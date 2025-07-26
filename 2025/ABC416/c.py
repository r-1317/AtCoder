import os
import itertools

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  N, K, X = map(int, input().split())
  S_list = [input().strip() for _ in range(N)]

  f_index_list = list(itertools.product(list(range(N)), repeat=K))

  ic(f_index_list)

  f_list = []

  for f_index in f_index_list:
    f = ""
    for i in f_index:
      f += S_list[i]
    f_list.append(f)

  ic(f_list)

  f_list.sort()

  ic(f_list)

  print(f_list[X-1])

if __name__ == "__main__":
  main()