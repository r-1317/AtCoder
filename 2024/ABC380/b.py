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
  s_list = list(input())

  ans_list = []
  count = 0

  for s in s_list:
    if s == "|":
      ans_list.append(count)
      count = 0
    elif s == "-":
      count += 1
  ans_list.append(count)

  print(*ans_list[1:-1])


if __name__ == "__main__":
  main()