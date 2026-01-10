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
  T = int(input())

  for _ in range(T):
    N, W = map(int, input().split())
    c_list = list(map(int, input().split()))
    taba_list = [0]*(2*W)

    for i in range(N):
      taba_list[i%(2*W)] += c_list[i]

    # ic(taba_list)

    cum_sum_list = [0]*(4*W+3)
    cum_sum_list.append(taba_list[0])
    for i in range(1, 4*W+3):
      cum_sum_list[i] = cum_sum_list[i-1] + taba_list[i%(2*W)]
    # ic(cum_sum_list)
    
    cost_list = [0]*(2*W)
    for i in range(2*W):
      start_idx = i
      end_idx = i + W
      cost_list[i] = cum_sum_list[end_idx] - cum_sum_list[start_idx]

    ic(min(cost_list))
    print(min(cost_list))

if __name__ == "__main__":
  main()