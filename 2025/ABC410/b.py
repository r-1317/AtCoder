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
  n, q = map(int, input().split())
  x_list = list(map(int, input().split()))

  box_list = [0] * (n + 1)
  box_list[0] = 10**9

  ans_list = []

  for x in x_list:
    if x != 0:
      box_list[x] += 1
      ans_list.append(x)
    else:
      min_count = min(box_list)
      for i in range(1, len(box_list)):
        if box_list[i] == min_count:
          box_list[i] += 1
          ans_list.append(i)
          break

  print(*ans_list)


if __name__ == "__main__":
  main()