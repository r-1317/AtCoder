import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def calc_imbalance(ans_list, x):
  x = max(x, max(ans_list) - min(ans_list))

  if len(ans_list) == 1:
    return x
  
  new_ans_list = []
  for i in range(0, len(ans_list), 2):
    new_ans_list.append(ans_list[i] + ans_list[i+1])
  return calc_imbalance(new_ans_list, x)

def main():
  N, K = map(int, input().split())

  index_list = [0]
  for i in range(N-1, -1, -1):
    stride = 2**i
    next_indx_queue = []
    for idx in index_list:
      next_indx_queue.append(idx + stride)

    for idx in next_indx_queue:
      index_list.append(idx)

    ic(index_list)

  mod_k = K % 2**N
  ic(mod_k)

  index_list = index_list[0:mod_k]

  index_set = set(index_list)

  ans_list = [K//(2**N)]*(2**N)

  for i in range(2**N):
    if i in index_set:
      ans_list[i] += 1

  imbalance = calc_imbalance(ans_list, 0)

  print(imbalance)
  print(*ans_list)

if __name__ == "__main__":
  main()