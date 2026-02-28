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
  N = int(input())
  a_list = list(map(int, input().split()))
  next_count_dict = dict()
  max_len = 0
  for a in a_list:
    if a in next_count_dict:
      length = next_count_dict.pop(a)
      length += 1
    else:
      length = 1
    if a+1 in next_count_dict:
      next_count_dict[a+1] = max(next_count_dict[a+1], length)
    else:
      next_count_dict[a+1] = length
    max_len = max(max_len, length)
  print(max_len)

if __name__ == "__main__":
  main()