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
  N, K = map(int, input().split())
  a_list = list(map(int, input().split()))

  first_idx_dict = dict()

  sum_count_list = [0]*N

  for i in range(N):
    a = a_list[i]
    if not a in first_idx_dict:
      first_idx_dict[a] = i
    sum_count_list[first_idx_dict[a]] += a

  ic(sum_count_list)

  sum_count_list.sort(reverse=True)

  print(sum(sum_count_list[K:]))

if __name__ == "__main__":
  main()