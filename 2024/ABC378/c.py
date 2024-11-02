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
  n = int(input())
  a_list = list(map(int, input().split()))
  index_dict = {}

  ans_list = [0]*n

  for i in range(n):
    if a_list[i] in index_dict:
      ans_list[i] = index_dict[a_list[i]]
    else:
      ans_list[i] = -1

    index_dict[a_list[i]] = i+1

  ic(index_dict)

  print(*ans_list)


if __name__ == "__main__":
  main()