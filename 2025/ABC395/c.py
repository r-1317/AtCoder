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

  num_index_list = [[] for _ in range(10**6+1)]
  min_len = 10**9

  for i, a in enumerate(a_list):
    if len(num_index_list[a]) != 0:
      min_len = min(min_len, i - num_index_list[a][-1] + 1)
    num_index_list[a].append(i)

  print(min_len if min_len != 10**9 else -1)

if __name__ == "__main__":
  main()