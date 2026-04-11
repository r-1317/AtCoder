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
  T, X = map(int, input().split())
  a_list = list(map(int, input().split()))

  hozon_list = []
  current = -10**9

  for i in range(T+1):
    a = a_list[i]

    if abs(current - a) >= X:
      hozon_list.append((i, a))
      current = a

  for row in hozon_list:
    print(*row)


if __name__ == "__main__":
  main()