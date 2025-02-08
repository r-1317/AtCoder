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
  a_list = list(map(int, input().split()))
  tmp_list = [True] * (n + 1)
  tmp_list[0] = False
  for a in a_list:
    tmp_list[a] = False
  ans_list = []
  for i in range(1, n + 1):
    if tmp_list[i]:
      ans_list.append(i)
  print(len(ans_list))
  print(*ans_list)


if __name__ == "__main__":
  main()