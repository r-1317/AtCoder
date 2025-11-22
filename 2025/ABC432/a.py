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
  A, B, C = map(int, input().split())

  ans = 0

  omomi = [1, 10, 100]

  for w_list in itertools.permutations(omomi, 3):
    ic(w_list)

    tmp = A*w_list[0] + B*w_list[1] + C*w_list[2]
    ans = max(tmp, ans)

  print(ans)

if __name__ == "__main__":
  main()