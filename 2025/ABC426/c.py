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
  N, Q = map(int, input().split())

  mini = 0

  count_list = [1]*(N+1)
  count_list[0] = 0

  for _ in range(Q):
    x, y = map(int, input().split())

    a = 0

    if x < mini:
      pass
    else:
      for i in range(mini, x+1):
        a += count_list[i]
      mini = x+1
      count_list[y] += a
    print(a)

if __name__ == "__main__":
  main()