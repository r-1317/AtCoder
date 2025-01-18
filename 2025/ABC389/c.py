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
  q = int(input())

  cum_sum_list = [0]*(3*10**5+1)
  front_index = 0
  back_index = 1

  for i in range(q):
    query_list = list(map(int, input().split()))
    # 1の場合
    if query_list[0] == 1:
      l = query_list[1]
      cum_sum_list[back_index] = cum_sum_list[back_index - 1] + l
      back_index += 1
    # 2の場合
    elif query_list[0] == 2:
      front_index += 1
    # 3の場合
    elif query_list[0] == 3:
      k = query_list[1]
      k_index = k + front_index - 1
      print(cum_sum_list[k_index] - cum_sum_list[front_index])

if __name__ == "__main__":
  main()